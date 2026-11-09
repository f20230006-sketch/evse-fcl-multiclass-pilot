from pathlib import Path
import shutil,json,re
import pandas as pd
R=Path('D:/EV-charging');OLD=R/'manuscripts/ieee_networking_letters_illustrated_2026_11_04';OUT=R/'manuscripts/ieee_networking_letters_extension_2026_11_09';OUT.mkdir(exist_ok=True)
for name in ['tables','figures']:shutil.copytree(OLD/name,OUT/name,dirs_exist_ok=True)
s=(OLD/'main.tex').read_text(encoding='utf-8')
s=s.replace('Published class-balancing reservoir sampling and matched centralized controls extend the allocation comparison on one charging dataset with constructed client profiles.', 'A separate delayed-client stress test finds an 11.42-point Slowloris gain from adding teacher distillation to RBR. Comparisons use one dataset with constructed clients.')
s=s.replace('The primary evaluation merges six scan labels while preserving Slowloris as a separate output.', 'The primary evaluation merges six scan labels while preserving Slowloris as a separate output. A separate exploratory stress test examines compatibility with teacher distillation under delayed client exposure.')
s=s.replace('\\input{tables/federated_split_results}', '')
s=s.replace('(Table~\\ref{tab:fedsplits})','(supporting tables)')
# Compact redundant CBRS implementation prose; full population rule remains in code and supporting records.
a=s.index('CBRS uses the published population rule');b=s.index('\\subsection{Scoring}',a)
s=s[:a]+r'''CBRS uses its published streaming population rule~\cite{cbrs}, with persistent full-class flags and encounter counters. It calibrates only the replay fraction at memory 60, original split 42, under the same backbone and loss. Population updates occur at task boundaries with uniform retrieval; the paper's separate weighted-replay recipe is outside this allocation comparison. All selection uses calibration data before evaluation.

'''+s[b:]
insert=r'''\subsection{Exploratory delayed-client extension}
A separate study uses split 63 of the reused corpus, the rare-first order $(L,V,F,R)$, and six global phases. Client starts are delayed by $(0,1,0,2,1)$ phases in profile order, preserving each client's four cohort exposures. Inactive clients do not train. Pooled controls match arrivals and total replay rows. Global update count and optimizer resets differ from synchronous training; this is a compound timing/participation stress test.

To examine complementary regularization, a frozen teacher captures the phase-start model. Temperature-2 KL divergence over previously available outputs is added to current/replay cross-entropy, weighted by the same batch fractions. The teacher stays fixed during that client's task and adds model RAM and computation, but no replay rows. This is an adaptation of established distillation~\cite{lwf}, not an allocation novelty claim. Distillation weight $\{0.1,1.0\}$, replay fraction and RBR quota are calibrated separately for five methods in both settings. Forty calibration fits precede 100 evaluations over ten seeds; complete settings and the earlier negative adaptive-quota study are retained in the supporting records.

'''
s=s.replace('\\section{Results}',insert+'\\section{Results}')
results=r'''\subsection{Distillation under delayed exposure}
\input{tables/distillation_results}
Table~\ref{tab:distill} is separate from the original protocol. Distilled RBR minus matched RBR gains are old accuracy $+4.99$ points $[1.05,8.93]$, Slowloris $+11.42$ $[1.63,21.20]$, and worst-client $+3.25$ $[0.29,6.21]$. Against distilled class-balanced replay, Slowloris improves $+9.60$ $[0.76,18.44]$; old accuracy $+1.58$ $[-1.50,4.66]$ and worst-client $-1.00$ $[-2.99,0.99]$ are not significant. Gains cannot be attributed solely to allocation.

Federated-minus-centralized distillation improvements are old accuracy $+4.79$ $[0.93,8.65]$ and Slowloris $+11.08$ $[1.05,21.11]$, exploratory interactions on one delayed order. A local calibration-driven quota variant on split 62 did not pass its prespecified federated screen. These repartitions reuse the same corpus and provide no independent external confirmation.

'''
s=s.replace('\\section{Conclusion}',results+'\\section{Conclusion}')
s=s.replace('Matched centralized controls show that these gains remain useful under the tested federated heterogeneity.', 'Matched centralized controls show that the allocation gains remain useful under the tested federated heterogeneity; exploratory delayed-client results motivate further study of complementary distillation.')
s=s.replace('EWC tuning is limited; intervals are unadjusted.', 'EWC tuning is limited; intervals are unadjusted. The delayed-client extension is exploratory and adds teacher state; it needs independent confirmation.')
s=s.replace('\\IEEEtriggeratref{4}','').replace('\\begin{thebibliography}{18}','\\begin{thebibliography}{19}')
s=s.replace('\\end{thebibliography}',r'''\bibitem{lwf} Z. Li and D. Hoiem, ``Learning without forgetting,'' in \emph{Proc. ECCV}, 2016, arXiv:1606.09282.
\end{thebibliography}''')
s=re.sub(r'\\begin\{figure\}\[t\].*?order_effects\.pdf.*?\\end\{figure\}', '', s, flags=re.S)
s=s.replace(r'Fig.~\ref{fig:orders} shows order variation.', 'Order-specific results vary (supporting records).')
(OUT/'main.tex').write_text(s,encoding='utf-8')
f=pd.read_csv(R/'outputs/distilled_replay_report_2026_11_09/summary.csv');f=f[(f.score_space=='merged_scans')&(f.environment=='federated')].set_index('method')
lines=[r'\begin{table}[t]',r'\centering',r'\caption{Exploratory delayed federated setting, split 63, memory 60/client. Mean $\pm$ SD over ten seeds (\%). KD is teacher distillation; CB is class-balanced.}',r'\label{tab:distill}',r'\footnotesize',r'\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{lrrr}',r'\toprule',r'Method & Old accuracy & Slowloris & Worst\\',r'\midrule']
for method,label in [('fixed_rbr','RBR'),('class_balanced_kd','CB + KD'),('fixed_rbr_kd','RBR + KD')]:
 row=f.loc[method];cells=[f"{100*row[m+'_mean']:.2f} $\\pm$ {100*row[m+'_std']:.2f}"for m in ['old_task_accuracy','slowloris_recall','worst_client_macro_recall']];lines.append(label+' & '+' & '.join(cells)+r'\\')
lines+=[r'\bottomrule',r'\end{tabular}',r'\end{table}'];(OUT/'tables/distillation_results.tex').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'README.md').write_text('# Manuscript extension\n\nSeparate manuscript incorporating the exploratory delayed-client distillation study. The original four-page paper and all accepted baseline results remain frozen in outputs/frozen_paper_2026_11_09. Existing primary tables are unchanged; new data use a separately described protocol and are not a replacement for the original comparison. A negative adaptive-quota study is disclosed. The teacher mechanism is established prior art. Author and affiliation fields remain pending confirmation.\n')
print(OUT)
