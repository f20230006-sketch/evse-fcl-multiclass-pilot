"""Populate the separate letter revision only from verified targeted tables."""
from pathlib import Path
import json,re
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/targeted_validation_report_2026_10_27';DOC=ROOT/'manuscripts/ieee_networking_letters_2026_10_27'
def main():
    assert json.loads((OUT/'verification.json').read_text())['status']=='passed'
    summary=pd.read_csv(OUT/'summary.csv');pairs=pd.read_csv(OUT/'paired_intervals.csv')
    def get(split,env,metric,left='balanced_rare_60',right='class_balanced_60',space='merged_scans'):
        return pairs[(pairs.split_seed==split)&(pairs.environment==env)&(pairs.metric==metric)&(pairs.left==left)&(pairs.right==right)&(pairs.order=='averaged')&(pairs.score_space==space)].iloc[0]
    def diff(r):return f"${r.mean_difference*100:+.2f}$ $[{r.ci95_low*100:.2f},{r.ci95_high*100:.2f}]$"
    rows=[]
    for split in [42,43,44,45]:
        for env in ['federated','centralized']:
            rows.append(f"{split} & {'Fed.' if env=='federated' else 'Central'} & "+' & '.join(diff(get(split,env,m)) for m in ['old_task_accuracy','slowloris_recall'])+r'\\')
    text=r'''\subsection{Additional splits and allocation ablation}
We repeat only class-balanced versus \BR\ at memory 60 with three additional role-split seeds, 43--45. The sampled traffic, seed-42 client allocation, original model, task orders and training settings remain fixed. For each split/order, Task-1 fitting preprocessing is refitted and frozen; both methods and environments share it. Each method selects replay settings on that split's calibration roles using the unchanged criterion, before any new evaluation. Ten training seeds and all three orders are retained.

\begin{table}[t]
\centering
\caption{Memory-60 \BR\ minus class-balanced, merged scores; percentage points [95\% paired interval]. Each row averages orders within ten paired training seeds.}
\label{tab:splits}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{llrr}
\toprule
Split & Setting & Old accuracy & Slowloris\\
\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule
\end{tabular}
\end{table}
'''
    for env in ['federated','centralized']:
        a=[get(s,env,'old_task_accuracy') for s in [42,43,44,45]];b=[get(s,env,'slowloris_recall') for s in [42,43,44,45]];w=[get(s,env,'worst_client_macro_recall') for s in [42,43,44,45]]
        text+=f"In the {env} setting, old-accuracy differences are positive on {sum(r.mean_difference>0 for r in a)}/4 splits and significant on {sum(r.outcome=='better' for r in a)}/4; Slowloris differences are positive on {sum(r.mean_difference>0 for r in b)}/4 and significant on {sum(r.outcome=='better' for r in b)}/4. Worst-client differences are significantly unfavorable on {sum(r.outcome=='worse' for r in w)}/4. "
    text+='Table~\\ref{tab:splits} and the accompanying evidence retain every split and per-order result.\n\n'
    text+=r'''The optional rare+random policy reserves a calibrated rare share and fills the rest uniformly, with no benign minimum. On the original split, its federated differences from protected are old accuracy '''+diff(get(42,'federated','old_task_accuracy','rare_random_60','protected_60'))+', Slowloris '+diff(get(42,'federated','slowloris_recall','rare_random_60','protected_60'))+', and worst-client '+diff(get(42,'federated','worst_client_macro_recall','rare_random_60','protected_60'))+'. '
    text+=r'''Against rare+random, \BR\ changes old accuracy by '''+diff(get(42,'federated','old_task_accuracy','balanced_rare_60','rare_random_60'))+', Slowloris by '+diff(get(42,'federated','slowloris_recall','balanced_rare_60','rare_random_60'))+', and worst-client by '+diff(get(42,'federated','worst_client_macro_recall','balanced_rare_60','rare_random_60'))+'. This comparison exposes the allocation trade-off; detailed selected quotas and all losses accompany the results.\n'
    (DOC/'tables/targeted_validation.tex').write_text(text)
    sensitivity=r'''\begin{table}[t]
\centering
\caption{Main memory-60 federated comparison in both views, original split. Percentages, mean $\pm$ SD; B is class-balanced, BR is balanced+rare.}
\label{tab:typeview}
\footnotesize
\setlength{\tabcolsep}{2pt}
\begin{tabular}{llrrrr}
\toprule
Method & View & Old acc. & Forget & Slowloris & Worst\\
\midrule
'''
    for space in ['merged_scans','original_type']:
        for method in ['class_balanced_60','balanced_rare_60']:
            r=summary[(summary.split_seed==42)&(summary.environment=='federated')&(summary.score_space==space)&(summary.method==method)].iloc[0]
            sensitivity+=('B' if method=='class_balanced_60' else 'BR')+' & '+('Merged' if space=='merged_scans' else 'Exact')+' & '+' & '.join(f"{100*r[m+'_mean']:.2f} $\\pm$ {100*r[m+'_std']:.2f}" for m in ['old_task_accuracy','forgetting','slowloris_recall','worst_client_macro_recall'])+r'\\'+'\n'
    sensitivity+=r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table}'+'\n'
    (DOC/'tables/type_sensitivity.tex').write_text(sensitivity)
    table=DOC/'tables/main_results.tex';t=table.read_text();t=t.replace('Federated final checkpoint, 60 examples/client.','Federated final checkpoint, original split 42, 60 examples/client.');table.write_text(t)
    s=(DOC/'main.tex').read_text()
    if r'\input{tables/type_sensitivity}' not in s:s=s.replace(r'\input{tables/main_results}',r'\input{tables/main_results}'+'\n'+r'\input{tables/type_sensitivity}')
    # Idempotently replace abstract and limitations; preserve all original numerical tables.
    abstract='Small replay memories must preserve earlier intrusion patterns while retaining infrequent attacks. We combine a fixed rare-group reservation with class-balanced local replay for continual flow classification in electric-vehicle charging networks. On the original split, at 60 examples per client, the policy improves old-attack accuracy by 1.53 percentage points and Slowloris recall by 5.06 points over class-balanced replay. Both gains remain significant under federation on each additional split. The study uses merged-Scan primary scores and exact-type sensitivity on one charging dataset with constructed client profiles.'
    s=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda _:r'\begin{abstract}'+'\n'+abstract+'\n'+r'\end{abstract}',s,flags=re.S)
    a=s.index('\\section{Limitations');b=s.index('\\begin{thebibliography}',a)
    limitations=r'''\section{Limitations}
The random role splits overlap and reuse one dataset with constructed clients; their intervals quantify training variability rather than independent capture generalization. Source filenames provide provenance groups, and flow IDs, expiration codes and timestamps are available, but no explicit session/capture column was found. The sampled traffic spans 59 scenario files, with only two benign and two Slowloris files. Whole-file assignment to three disjoint roles would leave these classes unsupported in at least one role. A file-held-out design is possible with different support/roles, but was not built in this scope.

There are only 16 benign and five fragmentation evaluation rows, so we make no false-alarm or fragmentation claims. The benign-starved profile has no benign evaluation support. Worst-client macro recall excludes unsupported labels, and non-significant intervals do not establish non-inferiority. Order-specific categorical vocabularies are fitted on the first task, so order differences mix task order and representation effects; additional splits also change fitted vocabulary. Offline shared preprocessing is not a distributed privacy protocol.

The rare+random ablation calibrates its quota while protected fixed 20\%; within-rare sampling also differs from \BR. It compares allocation policies rather than fully isolating benign-quota causality. EWC's $\lambda\in\{1,100\}$ calibration grid is limited and not a claim of optimal EWC tuning. Public FedCBDR code exists, but the inspected commit lacks directly imported modules and its README method is absent from the dispatcher; adapting the image/CUDA implementation to this tabular protocol requires reconstruction. Superiority over FedCBDR, CBRS or other untested methods is not claimed.

Intervals are unadjusted for multiple comparisons. The memory budget counts replay rows, not total process RAM. We do not evaluate deployment latency, communication cost, energy, privacy leakage, adversarial evasion, or client dropout. The memory-300 protected-over-uniform Slowloris federation interaction remains exploratory. Original capacity/order losses remain part of the evidence, and the separate larger-model exploratory tuning does not replace this fixed protocol.

\section{Conclusion}
A predeclared rare-group reservation with a balanced remainder improves old-attack retention and Slowloris recall over class-balanced replay. Both federated gains are significant on the original and each additional role split at memory 60. Matched centralized comparisons also favor the policy in direction, with significance varying across splits. The allocation ablation exposes the different retention--Slowloris trade-off of random filling. The contribution is an evaluated local replay-allocation policy for charging-network flow classification.

'''
    s=s[:a]+limitations+s[b:]
    # Move short procedural caveats into the dedicated limitations section.
    s=s.replace(' These are synthetic label partitions, not five independently captured stations.',' These are constructed client profiles.').replace(' Order effects therefore include differences in initial representation as well as stream order.','').replace(' This offline preparation is not claimed as a privacy-preserving distributed preprocessing protocol.','')
    s=s.replace(' They are unadjusted for multiple comparisons and characterize training randomness on one split.',' Intervals characterize paired training-seed variability within each split.').replace(' Non-significance does not establish equivalence or non-inferiority.','')
    s=s.replace(' The worst-client interval spans zero and does not establish non-inferiority.','')
    s=s.replace(' No false-alarm improvement can be inferred because that client\'s benign support is zero. Classes with zero support are omitted from macro recall, so comparisons across clients have different supported-class compositions.','')
    s=s.replace('This shows partial separability, not intrinsic indistinguishability. ','')
    s=s.replace(' Its public checkout was inspected, but does not provide a directly runnable tabular MLP baseline.','')
    s=s.replace('This is a different retention--recall compromise, not uniform dominance.','This exposes a retention--recall trade-off.')
    s=s.replace('Federated \\BR\\ minus class-balanced differences by order and capacity.','Federated \\BR\\ minus class-balanced differences by order and capacity, original split 42.')
    # IEEE numbering follows first appearance, including the expanded related work.
    entries=dict(re.findall(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})',s,re.S))
    ordered=[]
    for group in re.findall(r'\\cite\{([^}]+)\}',s):
        for key in group.split(','):
            if key not in ordered:ordered.append(key)
    assert set(ordered)==set(entries)
    a=s.index('\\begin{thebibliography}');b=s.index('\\end{thebibliography}',a)
    s=s[:a]+'\\begin{thebibliography}{17}\n'+''.join('\\bibitem{'+key+'}'+entries[key] for key in ordered)+s[b:]
    (DOC/'main.tex').write_text(s)
    (DOC/'AUTHOR_NOTES.md').write_text('# Revised draft notes\n\nThe accepted 64/32 protocol is retained; exploratory tuned-model results are excluded. All additional splits and ablation results are frozen once, including losses. Author names, affiliations and contact details still need confirmation. This is a working draft, not submitted.\n')
    print('Revised manuscript source and data-driven additions generated; abstract words',len(abstract.split()))
if __name__=='__main__':main()
