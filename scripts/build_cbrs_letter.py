"""Build a concise evidence-driven letter after CBRS verification."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
import numpy as np
import pandas as pd
OUT=ROOT/'manuscripts/ieee_networking_letters_cbrs_2026_10_28'
REPORT=ROOT/'outputs/cbrs_report_2026_10_28'
METRICS=['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall']
def main():
    assert json.loads((REPORT/'verification.json').read_text())['status']=='passed'
    OUT.mkdir(exist_ok=True,parents=True);(OUT/'tables').mkdir(exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    summary=pd.read_csv(REPORT/'summary.csv');pairs=pd.read_csv(REPORT/'paired_intervals.csv')
    source=summary[(summary.environment=='federated')&(summary.score_space=='merged_scans')].set_index('method')
    def cell(r,m):return '--' if pd.isna(r[m+'_mean']) else f"{100*r[m+'_mean']:.2f} $\\pm$ {100*r[m+'_std']:.2f}"
    methods=[('no_replay','No replay'),('uniform_60','Uniform'),('class_balanced_60','Class-balanced'),('cbrs_60','CBRS'),('protected_60','Protected'),('balanced_rare_60','RBR'),('ewc','EWC'),('agem','A-GEM'),('joint','Joint')]
    def tab(path,caption,label,entries):
        rows=[r'\begin{table}[t]',r'\centering',r'\caption{'+caption+'}',r'\label{'+label+'}',r'\footnotesize',r'\setlength{\tabcolsep}{2.5pt}',r'\begin{tabular}{lrrrr}',r'\toprule',r'Method & Old acc. $\uparrow$ & Forget $\downarrow$ & Slowloris $\uparrow$ & Worst $\uparrow$\\',r'\midrule']
        for method,name in entries:rows.append(name+' & '+' & '.join(cell(source.loc[method],m) for m in METRICS)+r'\\')
        rows += [r'\bottomrule',r'\end{tabular}',r'\end{table}'];path.write_text('\n'.join(rows)+'\n')
    tab(OUT/'tables/main_results.tex',r'Federated memory 60/client, original split 42. Merged-Scan scores (\%); mean $\pm$ SD of ten seed averages over three orders. Worst is client macro recall.','tab:main',methods)
    tab(OUT/'tables/capacity_results.tex',r'Memory 300/client, same setting and scoring as Table~\ref{tab:main}.','tab:capacity',[(f'{m}_300',n) for m,n in [('class_balanced','Class-balanced'),('protected','Protected'),('balanced_rare','RBR')]])
    sensitivity=[r'\begin{table}[t]',r'\centering',r'\caption{Federated memory 60, original split. Both views (\%, mean $\pm$ SD); CB denotes class-balanced.}',r'\label{tab:type}',r'\footnotesize',r'\setlength{\tabcolsep}{1.5pt}',r'\begin{tabular}{llrrrr}',r'\toprule',r'Method & View & Old acc. & Forget & Slowloris & Worst\\',r'\midrule']
    for space,name in [('merged_scans','Merged'),('original_type','Exact')]:
        for method,label in [('class_balanced_60','CB'),('cbrs_60','CBRS'),('balanced_rare_60','RBR')]:
            r=summary[(summary.environment=='federated')&(summary.score_space==space)&(summary.method==method)].iloc[0];sensitivity.append(label+' & '+name+' & '+' & '.join(cell(r,m) for m in METRICS)+r'\\')
    sensitivity += [r'\bottomrule',r'\end{tabular}',r'\end{table}'];(OUT/'tables/type_results.tex').write_text('\n'.join(sensitivity)+'\n')
    validation=pd.read_csv(ROOT/'outputs/targeted_validation_report_2026_10_27/paired_intervals.csv')
    validation=validation[(validation.score_space=='merged_scans')&(validation.order=='averaged')&(validation.left=='balanced_rare_60')&(validation.right=='class_balanced_60')]
    rows=[r'\begin{table}[t]',r'\centering',r'\caption{RBR minus class-balanced at memory 60; percentage points [95\% paired interval].}',r'\label{tab:splits}',r'\footnotesize',r'\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{llrr}',r'\toprule',r'Split & Setting & Old accuracy & Slowloris\\',r'\midrule']
    def diff(r):return f"${r.mean_difference*100:+.2f}$ $[{r.ci95_low*100:.2f},{r.ci95_high*100:.2f}]$"
    for split in [42,43,44,45]:
        for env in ['federated','centralized']:
            r=validation[(validation.split_seed==split)&(validation.environment==env)].set_index('metric');rows.append(f"{split} & {'Fed.' if env=='federated' else 'Central'} & "+diff(r.loc['old_task_accuracy'])+' & '+diff(r.loc['slowloris_recall'])+r'\\')
    rows += [r'\bottomrule',r'\end{tabular}',r'\end{table}'];(OUT/'tables/split_results.tex').write_text('\n'.join(rows)+'\n')
    comparisons=[]
    for env in ['federated','centralized']:
        r=pairs[(pairs.score_space=='merged_scans')&(pairs.environment==env)&(pairs.order=='averaged')].set_index('metric')
        comparisons.append(('Federated' if env=='federated' else 'Centralized')+' RBR minus CBRS differences are old accuracy '+diff(r.loc['old_task_accuracy'])+', Slowloris '+diff(r.loc['slowloris_recall'])+', and worst-client '+diff(r.loc['worst_client_macro_recall'])+'.')
    loss=pairs[(pairs.score_space=='merged_scans')&(pairs.order=='averaged')&(pairs.outcome=='worse')]
    outcomes=' '.join(comparisons)
    if len(loss):outcomes+=' CBRS is significantly better on '+', '.join(r.environment+' '+r.metric.replace('_',' ') for r in loss.itertuples())+'.'
    for r in pairs[(pairs.score_space=='merged_scans')&(pairs.order!='averaged')&(pairs.outcome=='worse')].itertuples():
        outcomes+=' In '+r.environment+' order '+r.order[-1]+', the '+r.metric.replace('_',' ')+' difference is '+diff(r)+'.'
    exact=pairs[(pairs.score_space=='original_type')&(pairs.environment=='federated')&(pairs.order=='averaged')].set_index('metric')
    outcomes+=' With exact types, federated old-accuracy and Slowloris differences are '+diff(exact.loc['old_task_accuracy'])+' and '+diff(exact.loc['slowloris_recall'])+'; both intervals include zero.'
    template=r'''\documentclass[journal,10pt]{IEEEtran}
\usepackage{amsmath,amssymb,graphicx,booktabs,cite,url}
\newcommand{\RBR}{RBR}
\title{Rare-Reserved Balanced Replay for Federated Continual Intrusion Detection in EV Charging Networks}
\author{[Author names]\thanks{[Affiliations and contact information]}}
\markboth{Rare-Reserved Balanced Replay}{Federated Continual Intrusion Detection}
\begin{document}
\maketitle
\begin{abstract}
Small replay memories must preserve earlier intrusion patterns while retaining infrequent attacks. We evaluate rare-reserved balanced replay (RBR), which combines a fixed rare-group minimum with a class-balanced local remainder, for continual flow classification in electric-vehicle charging networks. At 60 examples per client, RBR improves old-attack accuracy by 1.53 percentage points and Slowloris recall by 5.06 points over class-balanced replay on the original split. Both federated gains remain significant on additional splits. Published class-balancing reservoir sampling and matched centralized controls extend the allocation comparison on one charging dataset with constructed client profiles.
\end{abstract}
\begin{IEEEkeywords}
Federated learning, continual learning, intrusion detection, replay memory, electric vehicle charging.
\end{IEEEkeywords}
\section{Introduction}
Charging stations depend on networked control and monitoring, making communication availability a security concern~\cite{ocpp,dataset}. Slowloris keeps incomplete HTTP requests open to consume server connection resources~\cite{slowloris}. Missing low-rate behavior can leave a service-disruption threat undetected even without a large traffic burst. A charging-network detector therefore needs to retain recognition of infrequent, previously encountered patterns as new attack classes arrive.

Federated training supports a shared detector while traffic remains at clients. D-IoT demonstrates federated IoT anomaly detection~\cite{diot}, and Kitsune studies online traffic anomaly detection~\cite{kitsune}. Continual intrusion detection also addresses forgetting and class imbalance through replay~\cite{amr}. We study how bounded client memories should allocate stored fitting flows under heterogeneous attack exposure.

Our contributions are: (i) a local rare-group reservation followed by a feasible class-balanced remainder; (ii) matched federated/centralized comparisons against uniform, class-balanced, protected and published CBRS population policies; and (iii) retention, Slowloris and worst-client results across memory capacities, attack orders and additional data-role splits.

\subsection{Related work}
FedAvg~\cite{fedavg}, FedProx~\cite{fedprox} and SCAFFOLD~\cite{scaffold} address distributed optimization; FedWeIT~\cite{fedweit} supports continual inter-client transfer. Small episodic memories~\cite{tiny} and exemplar-based incremental learning~\cite{icarl} motivate strong replay controls. GEM~\cite{gem}, A-GEM~\cite{agem}, EWC~\cite{ewc} and dark experience replay~\cite{der} modify gradients, regularization or stored targets.

CBRS balances a streaming reservoir and admits an importance-weighted extension~\cite{cbrs}; augmented replay studies imbalance-aware population and retrieval for IDS~\cite{amr}. RBR uses an explicit rare-group minimum followed by balanced task-boundary allocation. FedCBDR coordinates memory construction globally and changes logit scaling~\cite{fedcbdr}; RBR uses local candidates and the shared replay loss, with no allocation-related communication.

\section{Setting and Replay Allocation}
\subsection{Tasks and client profiles}
The MLP predicts benign and 14 attack types. Four cohorts are reconnaissance $R$ (aggressive, OS fingerprinting, SYN stealth, service-version and TCP-port scans), flooding $F$ (SYN, TCP, UDP, ICMP, PSHACK and synonymous-IP floods), low-rate/rare $L$ (Slowloris and ICMP fragmentation), and vulnerability scan $V$. Orders are $(R,F,L,V)$, $(F,R,V,L)$ and $(L,V,F,R)$. Benign fitting flows recur in each task. Unseen outputs are masked until their classes arrive.

Five constructed profiles emphasize reconnaissance, flooding or rare traffic, or are mixed or benign-starved. Table~\ref{tab:allocation} gives allocation weights; floors and largest-remainder redistribution assign each row to one client. All clients participate each round, and the global model is evaluated on each client's held-out flows.
\begin{table}[t]
\centering
\caption{Label-dependent client allocation weights (\%). Vulnerability uses the rare allocation row but is outside the reserved group.}
\label{tab:allocation}
\footnotesize
\begin{tabular}{lrrrrr}
\toprule
Group & Recon. & Flood & Rare & Mixed & Starved\\
\midrule
Benign &55&15&10&20&0\\
Reconnaissance &55&10&5&20&10\\
Flooding &10&55&5&20&10\\
Rare / vulnerability &5&5&55&25&10\\
\bottomrule
\end{tabular}
\end{table}

\subsection{Rare-reserved balanced replay}
At a task boundary, client $k$ forms candidates $C=\operatorname{unique}(M_{k,t-1}\cup D_{kt})$ from retained memory and current fitting rows. Let $B$ be capacity, $\mathcal G=\{\text{Slowloris},\text{ICMP fragmentation}\}$, and $\operatorname{Bal}(S,b)$ draw equal feasible quotas by cycling through original class labels, redistributing exhausted-class slots. RBR first reserves
\begin{align}
A&=\operatorname{Bal}(C^{\mathcal G},\min(\lfloor qB\rfloor,|C^{\mathcal G}|)),\\
M_{kt}&=A\cup\operatorname{Bal}(C\setminus A,B-|A|).
\end{align}
The balanced remainder includes benign and rare classes, so $q$ is a minimum reservation. Memory contains unique fitting flows and never exceeds $B$. Discarded history cannot re-enter except when it belongs to the current task's recurring benign reference.

With replay fraction $r$, local training minimizes $(1-r)\ell_{\rm current}+r\ell_{\rm replay}$ using cross-entropy and uniform sampling from retained rows. FedAvg weights updates by distinct current-plus-memory fitting counts. The centralized control pools all clients' fitting data and receives capacity $5B$, matching total replay storage.

\section{Experimental Protocol}
We cap each attack type at 3,000 available flows. The fixed sample has 36,172 rows: 23,513 fitting, 5,425 calibration and 7,234 evaluation. Persistent roles are stratified within client/type blocks using target fractions 0.65/0.15/0.20. Preprocessing excludes provenance, addresses, identifiers, absolute timestamps and fingerprint-like fields; scaling and categorical vocabularies fit only Task-1 fitting rows and then freeze. The backbone is input--64--32--15, ReLU and Adam, with five local epochs per round, five rounds per task, batch 128, weight decay $10^{-4}$ and no gradient clipping.

\subsection{Comparators and calibration}
The replay comparison varies memory allocation under a fixed replay loss. EWC, A-GEM and DER++ modify regularization, gradients or replay targets; their mechanisms are complementary and could be combined with the allocation rule. We report EWC and A-GEM as additional learning references. Joint fitting uses all tasks' fitting rows from the start.

Uniform replay samples candidates randomly; class-balanced applies $\operatorname{Bal}$ to the whole pool. Protected reserves 20\% each for benign and the rare group, then fills randomly. RBR calibrates $q\in\{0.10,0.20\}$; replay methods calibrate $r\in\{0.25,0.50\}$ at learning rate 0.003. Choices maximize mean-checkpoint original-type calibration macro recall, separately for each environment/order/capacity. Fine-tuning and joint calibrate learning rate in $\{0.001,0.003\}$; EWC calibrates $\lambda\in\{1,100\}$ and A-GEM reference batch size in $\{32,64\}$.

CBRS uses the published population rule~\cite{cbrs}: once memory is filled, non-full classes replace a random member of a largest class, while full classes use within-class reservoir replacement with probability $m_c/n_c$. A class remains full after becoming largest in filled memory. Each fitting flow enters the population stream once, counters persist, and population updates occur at the shared task boundary. CBRS calibrates only $r$ on original split 42, at $B=60$, under the same backbone and replay loss. All settings are selected before evaluation.

\subsection{Scoring}
Primary scoring sums six scan probabilities into one Scan output: the five reconnaissance types and vulnerability scan. Slowloris remains separate; original type labels and task cohorts are retained for training. A scan-only Random Forest achieves 34.25\% evaluation accuracy while fitting perfectly, motivating merged reporting alongside exact-type sensitivity.

Old accuracy averages final attack accuracy over the first three original cohorts. Forgetting averages each cohort's maximum post-learning accuracy minus its final accuracy. Slowloris recall uses its 600 evaluation flows. Worst-client score is the minimum supported-class macro recall. We report means and sample SD over ten training-seed averages of three orders; paired 95\% $t_9$ intervals use the ten seed differences. Additional role-split seeds 43--45 preserve the sample, allocation and settings, refit Task-1 preprocessing, and recalibrate the key RBR/class-balanced comparison at $B=60$.

\section{Results}
\input{tables/main_results}
\input{tables/type_results}
\subsection{Retention and Slowloris at memory 60}
RBR reaches 85.52\% old accuracy and 76.62\% Slowloris recall. Over class-balanced, gains are $+1.53$ points $[0.23,2.84]$ for old accuracy and $+5.06$ $[1.27,8.84]$ for Slowloris; forgetting falls by 1.54 points. Worst-client difference is $+1.06$ $[-0.07,2.19]$. Exact-type scores appear in Table~\ref{tab:type}.

Against protected, RBR gains 12.68 points of old accuracy and 31.87 of worst-client score, while losing 6.11 points of Slowloris. The rare+random/no-benign ablation reaches 72.07\% old accuracy, 84.78\% Slowloris and 48.62\% worst-client score: RBR changes these by $+13.45$, $-8.16$ and $+30.41$ points, respectively, with all three paired intervals excluding zero. This exposes the retention--Slowloris trade-off of random filling.

@CBRS_RESULTS@

\subsection{Capacity, order and federation}
\input{tables/capacity_results}
At memory 300, RBR improves old accuracy, Slowloris and worst-client score over class-balanced by 1.68, 5.94 and 0.42 points, respectively; each interval excludes zero. Protected exceeds RBR on old accuracy and Slowloris by 1.30 and 5.08 points, while RBR retains a 6.19-point worst-client advantage.
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/order_effects.pdf}
\caption{RBR minus class-balanced by order and capacity, original split. Bars are paired 95\% intervals over ten seeds.}
\label{fig:orders}
\end{figure}
Fig.~\ref{fig:orders} shows order variation. At memory 60, Slowloris gains are 11.60, 0 and 3.57 points across the three orders; order 2 ends with the rare cohort, where both methods reach full recall. At memory 300, RBR loses old accuracy to protected in orders 1 and 2.

The gains hold under federated heterogeneity and align with centralized controls at matched total storage. Centralized RBR gains over class-balanced at memory 60 are 1.67 points of old accuracy and 5.00 of Slowloris. Federated-minus-centralized differences in improvement are $-0.14$ $[-1.54,1.26]$ and $+0.06$ $[-4.26,4.38]$, respectively. Table~\ref{tab:splits} shows positive retention and Slowloris differences on all four splits in both settings; both federated gains are significant on each split. Centralized significance varies across splits. The rare-heavy/benign-starved profiles have RBR macro recall 79.25/88.55\%, versus 78.30/88.58\% with class-balanced replay.
\input{tables/split_results}

\section{Limitations and Conclusion}
The overlapping random splits use one dataset and constructed clients, not independent captures. Source filenames provide file groups, but no explicit session/capture column was found; only two benign and two Slowloris files prevent all three roles from having whole-file support. Sixteen benign and five fragmentation evaluation flows preclude false-alarm and fragmentation claims. Task-1 categorical vocabularies differ by order, mixing representation and order effects. Client results are descriptive; non-significance does not establish non-inferiority, and intervals are unadjusted for multiple comparisons.

CBRS population is assessed under the shared task-boundary training protocol and uniform replay retrieval; the original paper's separate weighted-replay training recipe is outside this comparison. Its federated retention/Slowloris significance depends on merged scoring. The rare+random ablation also varies calibrated quotas and within-group sampling, limiting single-component causal attribution. EWC was calibrated over a limited lambda range. FedCBDR's public image/CUDA checkout requires reconstruction for a faithful tabular baseline. Replay capacity counts rows, not total RAM; deployment, attack blocking and privacy guarantees are not measured.

RBR improves retention and Slowloris over class-balanced across the tested federated splits. Published CBRS and allocation ablations sharpen the comparison, while all losses remain part of the evidence. The result is a local replay-allocation policy evaluated under heterogeneous charging-network flow distributions.

\noindent\textbf{Code and data availability.} Code, configurations and split manifests: \url{https://github.com/f20230006-sketch/evse-fcl-multiclass-pilot} (private repository; access required). Dataset source:~\cite{dataset}.

@REFERENCES@
\end{document}
'''
    old=(ROOT/'manuscripts/ieee_networking_letters_2026_10_27/main.tex').read_text();entries=dict(re.findall(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})',old,re.S))
    entries['diot']=entries['diot'].replace('D'+chr(92)+chr(34)+'IoT','D-IoT')
    entries['slowloris']=r" R. Giobbi, ``Mitigating Slowloris,'' 2009. [Online]. Available: \url{https://www.sei.cmu.edu/blog/mitigating-slowloris/}"+'\n'
    template=template.replace('@CBRS_RESULTS@',outcomes)
    ordered=[]
    for group in re.findall(r'\\cite\{([^}]+)\}',template):
        for key in group.split(','):
            if key not in ordered:ordered.append(key)
    assert set(ordered)==set(entries)
    refs='\\IEEEtriggeratref{12}\n\\begin{thebibliography}{18}\n'+''.join('\\bibitem{'+key+'}'+entries[key] for key in ordered)+'\\end{thebibliography}\n'
    (OUT/'main.tex').write_text(template.replace('@REFERENCES@',refs),encoding='utf-8')
    # Re-render only an existing frozen figure: same data, consistent method name.
    sys.path.append(str(ROOT/'work/followup_plot_dependencies'))
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data=pd.read_csv(ROOT/'manuscripts/ieee_networking_letters_2026_10_27/figures/order_effects_data.csv');data.to_csv(OUT/'figures/order_effects_data.csv',index=False)
    plt.rcParams.update({'font.size':8,'axes.labelsize':8,'pdf.fonttype':42})
    fig,axes=plt.subplots(1,2,figsize=(3.5,2.1),sharey=True)
    for ax,cap in zip(axes,[60,300]):
        for metric,color,label,offset in [('old_task_accuracy','#2166ac','Old accuracy',-.08),('slowloris_recall','#bb4b13','Slowloris',.08)]:
            d=data[(data.capacity==cap)&(data.metric==metric)].sort_values('order');mean=d.mean_difference.to_numpy()*100;lo=d.ci95_low.to_numpy()*100;hi=d.ci95_high.to_numpy()*100
            ax.errorbar(np.arange(1,4)+offset,mean,yerr=[mean-lo,hi-mean],fmt='o',markersize=3,capsize=2,linewidth=.9,color=color,label=label)
        ax.axhline(0,color='#555',ls='--',lw=.7);ax.set_xticks([1,2,3]);ax.set_xlabel('Attack order');ax.set_title(f'Memory {cap}/client');ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    axes[0].set_ylabel('RBR minus class-balanced (points)');handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=2,frameon=False);fig.tight_layout(rect=(0,0,1,.88),pad=.5);fig.savefig(OUT/'figures/order_effects.pdf',bbox_inches='tight');fig.savefig(OUT/'figures/order_effects.png',dpi=180,bbox_inches='tight');plt.close(fig)
    files=[REPORT/'summary.csv',REPORT/'paired_intervals.csv',ROOT/'outputs/targeted_validation_report_2026_10_27/paired_intervals.csv',ROOT/'manuscripts/ieee_networking_letters_2026_10_27/figures/order_effects_data.csv']
    (OUT/'evidence_manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
    print('Letter source, tables and consistently named figure prepared. Main-source words:',len(template.split()))
if __name__=='__main__':main()
