# Targeted validation results - 27 October 2026

## What was done

- Repeated the key memory-60 comparison on three additional persistent-role splits, using the accepted model and calibration-only selection.
- Added rare reservation with random remainder and no benign quota on the original split.
- Re-scored merged-Scan and exact-type views, checked grouping metadata and inspected public FedCBDR code.
- Revised the letter with the validation results, allocation ablation and 17 references.

## Main results

Federated, original split; percentages, mean +/- SD of ten seed averages across three orders.

| Method | Old accuracy | Forgetting | Slowloris | Worst-client |
|---|---|---|---|---|
| Class-balanced | 83.99 +/- 1.44 | 15.77 +/- 1.42 | 71.56 +/- 4.19 | 77.97 +/- 1.05 |
| Protected | 72.84 +/- 2.25 | 26.84 +/- 2.29 | 82.73 +/- 2.36 | 47.15 +/- 3.82 |
| Balanced+rare | 85.52 +/- 1.27 | 14.24 +/- 1.27 | 76.62 +/- 4.16 | 79.03 +/- 1.00 |
| Rare+random | 72.07 +/- 2.87 | 27.60 +/- 2.90 | 84.78 +/- 2.04 | 48.62 +/- 5.37 |

## Cross-split comparisons

Balanced+rare minus class-balanced, percentage points [95% paired interval]. Each split uses ten paired training seeds averaged across the three orders. An interval excluding zero is significant; negative forgetting is better.

| Split | Setting | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| 42 | Fed. | +1.53 [+0.23, +2.84] | +5.06 [+1.27, +8.84] | +1.06 [-0.07, +2.19] |
| 42 | Central | +1.67 [+1.12, +2.22] | +5.00 [+3.04, +6.96] | +0.64 [+0.14, +1.14] |
| 43 | Fed. | +2.23 [+0.95, +3.51] | +7.93 [+4.03, +11.83] | +0.64 [-0.62, +1.91] |
| 43 | Central | +1.11 [+0.47, +1.74] | +3.48 [+1.31, +5.65] | +1.39 [-0.91, +3.69] |
| 44 | Fed. | +3.37 [+2.11, +4.63] | +11.28 [+7.59, +14.97] | +1.39 [+0.29, +2.49] |
| 44 | Central | +1.13 [-0.19, +2.46] | +3.80 [-0.79, +8.39] | -0.06 [-0.68, +0.55] |
| 45 | Fed. | +2.06 [+0.40, +3.72] | +6.09 [+1.30, +10.88] | +0.93 [-0.40, +2.25] |
| 45 | Central | +0.82 [+0.01, +1.63] | +2.61 [-0.01, +5.22] | -0.17 [-0.94, +0.60] |

## What this means

Federated: old-accuracy differences are positive on 4/4 splits, significantly better on 4/4; Slowloris differences are positive on 4/4, significantly better on 4/4. Worst-client score is significantly worse on 0/4.

Centralized: old-accuracy differences are positive on 4/4 splits, significantly better on 3/4; Slowloris differences are positive on 4/4, significantly better on 2/4. Worst-client score is significantly worse on 0/4.

## Allocation ablation

Original split, federated differences [95% interval].

| Comparison | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|
| Rare+random - Protected | -0.76 [-3.06, +1.54] | +2.05 [+0.69, +3.41] | +1.47 [-2.19, +5.12] |
| Balanced+rare - Rare+random | +13.45 [+10.83, +16.06] | -8.16 [-11.62, -4.71] | +30.41 [+26.61, +34.21] |

## Exact-type sensitivity

Original split, balanced+rare minus class-balanced [95% interval].

| Setting | View | Old accuracy | Slowloris | Worst-client |
|---|---|---|---|---|
| Fed. | Merged | +1.53 [+0.23, +2.84] | +5.06 [+1.27, +8.84] | +1.06 [-0.07, +2.19] |
| Fed. | Exact | +1.90 [+0.37, +3.43] | +6.02 [+1.51, +10.54] | +0.70 [-0.04, +1.45] |
| Central | Merged | +1.67 [+1.12, +2.22] | +5.00 [+3.04, +6.96] | +0.64 [+0.14, +1.14] |
| Central | Exact | +0.83 [+0.05, +1.61] | +3.72 [+2.04, +5.39] | +0.34 [+0.10, +0.58] |

## Evidence scope

The extra splits reuse overlapping flows from the same dataset, not new captures. Source filenames are available provenance groups, but no explicit session/capture column was found. Flow IDs and timestamps are not established session groups. File-level coverage is documented; no new splitting pipeline was built. Benign evaluation remains 16 flows and fragmentation five, so neither false-alarm nor fragmentation gains are claimed. The class-balanced and rare reservations operate on original types even for merged reporting.

Public FedCBDR code exists but the inspected checkout has missing imported modules, an unsupported README method name, and an image/CUDA pipeline. It was not reconstructed or presented as a baseline. Our allocation is local, with no additional coordination messages, whereas FedCBDR uses global memory coordination and objective/logit balancing.

All 132 calibration fits precede all 420 new evaluation runs. Saved models, roles, replay boundaries, 8280160 checkpoint prediction rows and 448 intervals passed verification. No exploratory tuned-model results replace the accepted protocol.


# Full tables


## summary.csv

| split_seed | score_space | environment | method | old_task_accuracy_mean | old_task_accuracy_std | forgetting_mean | forgetting_std | slowloris_recall_mean | slowloris_recall_std | worst_client_macro_recall_mean | worst_client_macro_recall_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | merged_scans | centralized | balanced_rare_60 | 0.916950409525258 | 0.0089312961095637 | 0.0770764264861449 | 0.0104920177762745 | 0.8836111111111112 | 0.0222256941732194 | 0.8551922699214366 | 0.0103397917766406 |
| 42 | merged_scans | centralized | class_balanced_60 | 0.9002533784271828 | 0.0087293420400734 | 0.094299351549875 | 0.0102371558200441 | 0.8336111111111111 | 0.029279470281625 | 0.8487779214098659 | 0.0097364639289126 |
| 42 | merged_scans | centralized | protected_60 | 0.8048170981252447 | 0.0161911077318567 | 0.1928001439532863 | 0.0164052007063815 | 0.9037222222222224 | 0.0180706015182623 | 0.6027005149377371 | 0.0390983766263533 |
| 42 | merged_scans | centralized | rare_random_60 | 0.8097671094068343 | 0.0217015598667062 | 0.1865865624635862 | 0.0216237709107402 | 0.8809444444444445 | 0.0320579572029696 | 0.6374275080166747 | 0.0309065905911505 |
| 42 | merged_scans | federated | balanced_rare_60 | 0.8552136256407927 | 0.0126598540484429 | 0.1423799450112668 | 0.012730584486781 | 0.7661666666666667 | 0.0415735172774724 | 0.7902764249639249 | 0.0099881203613823 |
| 42 | merged_scans | federated | class_balanced_60 | 0.839886996304454 | 0.0143633358007434 | 0.1577325482139379 | 0.0142485709464446 | 0.7156111111111112 | 0.0419283551841702 | 0.7796629292929292 | 0.0104588214366881 |
| 42 | merged_scans | federated | protected_60 | 0.72838007027196 | 0.0224849182972023 | 0.268364038742025 | 0.0229237730015258 | 0.8272777777777778 | 0.0235839713302001 | 0.4715368265993266 | 0.0381765444437448 |
| 42 | merged_scans | federated | rare_random_60 | 0.7207415928182244 | 0.0287460973127608 | 0.2760416305996127 | 0.029005125171678 | 0.8477777777777777 | 0.020398969822559 | 0.4861895390412057 | 0.0536960389269331 |
| 42 | original_type | centralized | balanced_rare_60 | 0.551908428439521 | 0.0106882053277972 | 0.2683903390074497 | 0.011104196790772 | 0.8979444444444444 | 0.0125981741442776 | 0.5569134199134199 | 0.0055758030670196 |
| 42 | original_type | centralized | class_balanced_60 | 0.5436204403101305 | 0.0179136538109197 | 0.2777042211024952 | 0.0183166716180632 | 0.8607777777777776 | 0.0166938050657127 | 0.5535233285233285 | 0.0050216794481791 |
| 42 | original_type | centralized | protected_60 | 0.516116335365848 | 0.0158488389230281 | 0.3116083141200904 | 0.0162542089379549 | 0.9577777777777776 | 0.020576399175216 | 0.3956638287638288 | 0.0250016078415171 |
| 42 | original_type | centralized | rare_random_60 | 0.5108270791979781 | 0.019574564449008 | 0.3131636297094795 | 0.0205622693342656 | 0.9007777777777776 | 0.0323933302759207 | 0.4163245791245791 | 0.0211569178745275 |
| 42 | original_type | federated | balanced_rare_60 | 0.4957691145735076 | 0.0196698065450418 | 0.3307608809331586 | 0.0198926076575842 | 0.7827222222222223 | 0.05008528391948 | 0.5241240981240981 | 0.0068893023119541 |
| 42 | original_type | federated | class_balanced_60 | 0.4767616278648049 | 0.016755769355206 | 0.349738785952638 | 0.0166659096695621 | 0.7224999999999999 | 0.0411888237801175 | 0.517087012987013 | 0.007197738368449 |
| 42 | original_type | federated | protected_60 | 0.4278047090299752 | 0.0252251015689589 | 0.387972733317343 | 0.0276171263933945 | 0.8697222222222223 | 0.0256603460765472 | 0.3084531024531024 | 0.0255998860683648 |
| 42 | original_type | federated | rare_random_60 | 0.4267402446657281 | 0.0315387930092886 | 0.3910355713447014 | 0.0291327533199165 | 0.8711111111111111 | 0.0253548208633996 | 0.3147691197691197 | 0.0348966810302494 |
| 43 | merged_scans | centralized | balanced_rare_60 | 0.9091174663185374 | 0.0067545238330257 | 0.0870634062009224 | 0.0066832256625342 | 0.8336666666666666 | 0.029309848436379 | 0.7765123456790124 | 0.0361323242197467 |
| 43 | merged_scans | centralized | class_balanced_60 | 0.8980420272787922 | 0.0103720715792641 | 0.0983743385437921 | 0.0108691983029812 | 0.7988888888888889 | 0.0341022427849395 | 0.7626131687242799 | 0.0329682956571511 |
| 43 | merged_scans | federated | balanced_rare_60 | 0.8812348122933467 | 0.0104334574880013 | 0.1143415793676844 | 0.0111538567942735 | 0.7971111111111111 | 0.0307739668719688 | 0.7680284362139917 | 0.0151879151854591 |
| 43 | merged_scans | federated | class_balanced_60 | 0.8589251171055412 | 0.0154243631998571 | 0.138032787997242 | 0.0156284823115558 | 0.7178333333333333 | 0.0430908457523673 | 0.7615897685853241 | 0.0233815048102409 |
| 43 | original_type | centralized | balanced_rare_60 | 0.5390559100240149 | 0.0138465727622399 | 0.2835879254584079 | 0.0143917607607241 | 0.8683333333333334 | 0.0144539380008058 | 0.5015079365079365 | 0.0251175116760031 |
| 43 | original_type | centralized | class_balanced_60 | 0.5340313127351115 | 0.0150749450164983 | 0.2896984904918194 | 0.0153605756567324 | 0.843388888888889 | 0.0203239369775178 | 0.4929761904761904 | 0.0225644860049284 |
| 43 | original_type | federated | balanced_rare_60 | 0.5259307678358579 | 0.0168518654911674 | 0.2906442464147047 | 0.0176591914752261 | 0.8355 | 0.0434277619449193 | 0.499474074074074 | 0.0108928117874643 |
| 43 | original_type | federated | class_balanced_60 | 0.4798510988451127 | 0.0161360926734244 | 0.3463832066249801 | 0.016417410117131 | 0.7278333333333333 | 0.0386956840885154 | 0.4924154813440528 | 0.0146497649032174 |
| 44 | merged_scans | centralized | balanced_rare_60 | 0.9018547022589898 | 0.0136216653882835 | 0.0938593782721562 | 0.0150309065124008 | 0.8689444444444444 | 0.0381593385241159 | 0.861556491101491 | 0.0049734710396023 |
| 44 | merged_scans | centralized | class_balanced_60 | 0.8905279273337626 | 0.0157591110395307 | 0.1054155910653874 | 0.0168450672150799 | 0.8309444444444445 | 0.0425829699274999 | 0.8621745731120731 | 0.0073422498921549 |
| 44 | merged_scans | federated | balanced_rare_60 | 0.8735527066519524 | 0.0103448279336236 | 0.1224185839121179 | 0.0094753714250785 | 0.8215555555555556 | 0.028550727362395 | 0.8277916867083533 | 0.0152980371112881 |
| 44 | merged_scans | federated | class_balanced_60 | 0.8398248543831743 | 0.0124906817498616 | 0.1572613149162526 | 0.0128833106270993 | 0.7087777777777778 | 0.034473106354496 | 0.8138929773929775 | 0.006093652987581 |
| 44 | original_type | centralized | balanced_rare_60 | 0.5503924552325089 | 0.0141460544461848 | 0.2715873736916582 | 0.0133441876012001 | 0.8901666666666668 | 0.0189379355966779 | 0.5561750360750362 | 0.0057872018777047 |
| 44 | original_type | centralized | class_balanced_60 | 0.541418144341564 | 0.0128291689965462 | 0.280387402766768 | 0.0124498396559932 | 0.8586111111111112 | 0.0282226718152193 | 0.5573597883597884 | 0.007660860901897 |
| 44 | original_type | federated | balanced_rare_60 | 0.5310223952810954 | 0.0162536169153989 | 0.2855117052003303 | 0.0162817748973138 | 0.8497777777777777 | 0.0332428813919207 | 0.5412996632996634 | 0.0097509580852582 |
| 44 | original_type | federated | class_balanced_60 | 0.4964745408606374 | 0.0170757252336628 | 0.321285549467256 | 0.0179078524182933 | 0.7363333333333333 | 0.0190627438480883 | 0.535051467051467 | 0.0073603724345719 |
| 45 | merged_scans | centralized | balanced_rare_60 | 0.906327112296059 | 0.0126144581720365 | 0.0893287129712679 | 0.0140942404706813 | 0.8347777777777777 | 0.0378278535216791 | 0.8595286756453424 | 0.007259893667846 |
| 45 | merged_scans | centralized | class_balanced_60 | 0.8981408090195012 | 0.0088368463965831 | 0.0978849871148094 | 0.0093882708218656 | 0.8087222222222221 | 0.0230152481214201 | 0.8612031692587248 | 0.0126695606780899 |
| 45 | merged_scans | federated | balanced_rare_60 | 0.8795914607967047 | 0.0080150229148118 | 0.1183179185065918 | 0.00785174300763 | 0.7855 | 0.0152110213814774 | 0.8402584426273316 | 0.0087064021672449 |
| 45 | merged_scans | federated | class_balanced_60 | 0.8589982486665526 | 0.0233130355580294 | 0.1386186019646931 | 0.0240399613122981 | 0.7246111111111111 | 0.0694624914821524 | 0.8309897589653146 | 0.0125212290976583 |
| 45 | original_type | centralized | balanced_rare_60 | 0.5461599065918923 | 0.0217918081065583 | 0.2767152330311127 | 0.0231953195376265 | 0.8573333333333334 | 0.030885202728806 | 0.5559905174190888 | 0.0047545816223196 |
| 45 | original_type | centralized | class_balanced_60 | 0.5400915895521001 | 0.0165236855453818 | 0.2820794468638146 | 0.0168459724122852 | 0.8449444444444444 | 0.0225020194185977 | 0.5588894042465471 | 0.0087633183243916 |
| 45 | original_type | federated | balanced_rare_60 | 0.5040091699665697 | 0.0068473172393588 | 0.3225141058778961 | 0.0068917062244871 | 0.7946666666666666 | 0.0120760052988582 | 0.5471494949494949 | 0.0062314798455973 |
| 45 | original_type | federated | class_balanced_60 | 0.5002898016665057 | 0.0235720705337692 | 0.3181446492096131 | 0.0248294611885673 | 0.7581111111111112 | 0.0616881844340181 | 0.5411179894179894 | 0.0056398093681939 |

## paired_intervals.csv

| split_seed | score_space | environment | order | left | right | metric | outcome | n_seed_pairs | mean_difference | std_difference | ci95_low | ci95_high | significance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0153266293363387 | 0.0182487136434619 | 0.0022722860063967 | 0.0283809726662807 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.015352603202671 | 0.0183825922706275 | -0.0285027175331179 | -0.0022024888722242 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0505555555555555 | 0.0529538971779929 | 0.0126746195111877 | 0.0884364915999233 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0106134956709956 | 0.0158432184727311 | -0.0007200600762836 | 0.0219470514182749 | not significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.0076384774537355 | 0.0321622364579043 | -0.0306459554153772 | 0.015369000507906 | not significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0076775918575876 | 0.0325660233882213 | -0.0156187378731971 | 0.0309739215883724 | not significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | protected_60 | slowloris_recall | better | 10 | 0.0205 | 0.0189639937509194 | 0.0069339761054845 | 0.0340660238945155 | significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0146527124418791 | 0.0511346912467162 | -0.021926842076166 | 0.0512322669599243 | not significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.1344720328225684 | 0.036576037136747 | 0.1083071120637361 | 0.1606369535814006 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.1336616855883458 | 0.0367794604008476 | -0.1599721265839877 | -0.107351244592704 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.0816111111111111 | 0.0482828954937099 | -0.1161506138428238 | -0.0470716083793984 | significant |
| 42 | merged_scans | federated | averaged | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.3040868859227191 | 0.0531589891332179 | 0.266059235931822 | 0.3421145359136163 | significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.1191454034862296 | 0.0386713842351179 | -0.1468092452622883 | -0.0914815617101709 | significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.1183090823856747 | 0.0387033672336896 | 0.0906223613507141 | 0.1459958034206354 | significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1321666666666666 | 0.0403427105379994 | 0.1033072300777103 | 0.161026103255623 | significant |
| 42 | merged_scans | federated | averaged | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.2934733902517236 | 0.055448153558271 | -0.3331386098229861 | -0.2538081706804611 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.03581623933265 | 0.0370068583888774 | 0.0093431276158671 | 0.0622893510494328 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.03581623933265 | 0.0370068583888773 | -0.0622893510494328 | -0.0093431276158671 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.116 | 0.1204190215071553 | 0.0298574213545581 | 0.2021425786454419 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0293941991341991 | 0.0335082418197237 | 0.0054238469415057 | 0.0533645513268925 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0039063346862097 | 0.0801850528248208 | -0.0534545966076939 | 0.0612672659801134 | not significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0031783597676063 | 0.0804091194506653 | -0.0606995786697055 | 0.0543428591344928 | not significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | protected_60 | slowloris_recall | better | 10 | 0.029 | 0.0294622587619826 | 0.0079239697291042 | 0.0500760302708957 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | -0.0007716049382715 | 0.1335395107693238 | -0.0963000161871271 | 0.0947568063105839 | not significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.1309311271603279 | 0.1108976059721008 | 0.051599758872509 | 0.2102624954481468 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.1322545383838689 | 0.1110048213172576 | -0.2116626039092718 | -0.052846472858466 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.1775 | 0.1278653081841866 | -0.2689693312436979 | -0.0860306687563021 | significant |
| 42 | merged_scans | federated | order_1 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.349810125060125 | 0.1477083432195493 | 0.2441459416684513 | 0.4554743084517987 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0951148878276778 | 0.1001448207014727 | -0.1667541769137272 | -0.0234755987416284 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0964382990512188 | 0.1001009098838837 | 0.0248304218717786 | 0.1680461762306591 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.2935 | 0.0915923941529353 | 0.2279787483082586 | 0.3590212516917415 | significant |
| 42 | merged_scans | federated | order_1 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.3204159259259259 | 0.1389234289555521 | -0.4197957602304839 | -0.2210360916213678 | significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | protected_60 | old_task_accuracy | worse | 10 | -0.031097326400413 | 0.0217800145430843 | -0.0466778102159623 | -0.0155168425848637 | significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | protected_60 | forgetting | worse | 10 | 0.031097326400413 | 0.0217800145430843 | 0.0155168425848637 | 0.0466778102159623 | significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | 0.0296666666666666 | 0.0453164456562248 | -0.0027507656875837 | 0.0620840990209171 | not significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0427942119608786 | 0.0872211191931293 | -0.0196000180004664 | 0.1051884419222236 | not significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.2937995169082125 | 0.0169014973072398 | 0.2817089140882243 | 0.3058901197282008 | significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.2937995169082126 | 0.0169014973072398 | -0.3058901197282009 | -0.2817089140882244 | significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | 0.0005 | 0.0029449685068219 | -0.0016067035592228 | 0.0026067035592228 | not significant |
| 42 | merged_scans | federated | order_2 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.543801607343274 | 0.0665883894193612 | 0.4961671431146322 | 0.5914360715719158 | significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.2937995169082125 | 0.0169014973072398 | -0.3058901197282008 | -0.2817089140882243 | significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.2937995169082126 | 0.0169014973072398 | 0.2817089140882244 | 0.3058901197282009 | significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | -0.0005 | 0.0029449685068219 | -0.0026067035592228 | 0.0016067035592228 | not significant |
| 42 | merged_scans | federated | order_2 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.543801607343274 | 0.0665883894193612 | -0.5914360715719158 | -0.4961671431146322 | significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0101636486763663 | 0.0315888213462134 | -0.0124336328251389 | 0.0327609301778716 | not significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0102415702753632 | 0.0319714264333294 | -0.0331125509681966 | 0.0126294104174701 | not significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0356666666666666 | 0.0794937686819492 | -0.0211997497416454 | 0.0925330830749787 | not significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0024462878787878 | 0.033697041337403 | -0.0216591233527214 | 0.0265516991102972 | not significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0042755593529964 | 0.0225863630215202 | -0.0118817514152213 | 0.0204328701212142 | not significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0048861910600436 | 0.0256876203300226 | -0.0232620076610924 | 0.013489625541005 | not significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | 0.0028333333333333 | 0.0730214326730832 | -0.0494030528132701 | 0.0550697194799367 | not significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0019355303030303 | 0.0264491159608706 | -0.0169850274564124 | 0.020856088062473 | not significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | rare_random_60 | old_task_accuracy | worse | 10 | -0.0213145456008353 | 0.0217647353537521 | -0.0368840993427781 | -0.0057449918588924 | significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | rare_random_60 | forgetting | worse | 10 | 0.0250689985270439 | 0.0239272290995626 | 0.0079524899499159 | 0.0421855071041718 | significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.0678333333333333 | 0.0740955755830782 | -0.1208381150286017 | -0.0148285516380649 | significant |
| 42 | merged_scans | federated | order_3 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.0186489253647586 | 0.0222543381134384 | 0.0027291309074916 | 0.0345687198220256 | significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0314781942772016 | 0.0312723078377811 | 0.0091073328997865 | 0.0538490556546166 | significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | class_balanced_60 | forgetting | better | 10 | -0.0353105688024071 | 0.0317442334433538 | -0.0580190254208732 | -0.012602112183941 | significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1035 | 0.0789219414326977 | 0.0470426441634625 | 0.1599573558365374 | significant |
| 42 | merged_scans | federated | order_3 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0162026374859707 | 0.0238013387186547 | -0.0332290895097209 | 0.0008238145377793 | not significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.016697031098075 | 0.0077187767550406 | 0.0111753508407065 | 0.0222187113554435 | significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.01722292506373 | 0.0093975216377858 | -0.0239455070663342 | -0.0105003430611259 | significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.05 | 0.0274286704306136 | 0.0303787111858515 | 0.0696212888141484 | significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0064143485115707 | 0.007032991826517 | 0.0013832492388325 | 0.0114454477843089 | significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0049500112815895 | 0.028265859036043 | -0.0152701661830532 | 0.0251701887462323 | not significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0062135814897 | 0.0284352437194871 | -0.0265549294574103 | 0.0141277664780101 | not significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | -0.0227777777777777 | 0.03590109871423 | -0.0484598766749571 | 0.0029043211194016 | not significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0347269930789375 | 0.0490357400426672 | -0.0003510621999945 | 0.0698050483578696 | not significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.1071833001184237 | 0.0207705563799588 | 0.0923249391711552 | 0.1220416610656921 | significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.1095101359774413 | 0.0209752420060611 | -0.124514920200895 | -0.0945053517539876 | significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | 0.0026666666666666 | 0.0346655587034087 | -0.0221315801511679 | 0.0274649134845012 | not significant |
| 42 | merged_scans | centralized | averaged | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.2177647619047619 | 0.0302240200685249 | 0.1961438004225295 | 0.2393857233869943 | significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0904862690203486 | 0.0232530309742184 | -0.1071204853125187 | -0.0738520527281784 | significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0922872109137112 | 0.0231793090243301 | 0.0757057321275154 | 0.1088686896999071 | significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0473333333333333 | 0.0329054846350455 | 0.0237941676553233 | 0.0708724990113434 | significant |
| 42 | merged_scans | centralized | averaged | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.2113504133931911 | 0.0332108902835766 | -0.2351080531110006 | -0.1875927736753817 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0150280262114857 | 0.0165300336839534 | 0.0032031524597325 | 0.0268528999632389 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0150280262114857 | 0.0165300336839533 | -0.0268528999632389 | -0.0032031524597326 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0453333333333333 | 0.0506732451869601 | 0.0090838774408679 | 0.0815827892257987 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.005124068061568 | 0.0104015735466588 | -0.002316769408002 | 0.0125649055311381 | not significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.0077836927949501 | 0.0240274686359533 | -0.0249719084166865 | 0.0094045228267863 | not significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0080713352332729 | 0.0244988902386574 | -0.0094541150875818 | 0.0255967855541277 | not significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | protected_60 | slowloris_recall | worse | 10 | -0.1026666666666666 | 0.0545192230228232 | -0.1416673693642291 | -0.0636659639691042 | significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0407110718294051 | 0.0607095636541946 | -0.002717933789123 | 0.0841400774479333 | not significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | rare_random_60 | old_task_accuracy | worse | 10 | -0.0149261405351831 | 0.0178230583190083 | -0.0276759883892138 | -0.0021762926811525 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | rare_random_60 | forgetting | not significant | 10 | 0.0112338027409233 | 0.0183699992511329 | -0.0019073030860609 | 0.0243749085679076 | not significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.102 | 0.0580750897492437 | -0.1435444165170206 | -0.0604555834829793 | significant |
| 42 | merged_scans | centralized | order_1 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.0729120105820106 | 0.0521990525801355 | 0.0355710578336551 | 0.110252963330366 | significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0299541667466688 | 0.015749434390104 | 0.0186877000905671 | 0.0412206334027706 | significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | class_balanced_60 | forgetting | better | 10 | -0.0262618289524091 | 0.0163576671500037 | -0.037963399113743 | -0.0145602587910751 | significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1473333333333333 | 0.0459347363114234 | 0.114473602488989 | 0.1801930641776776 | significant |
| 42 | merged_scans | centralized | order_1 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.0677879425204425 | 0.0498982477330785 | -0.1034829986321636 | -0.0320928864087214 | significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0142417892834752 | 0.0609931188028577 | -0.0293900594688728 | 0.0578736380358234 | not significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0142862337279197 | 0.0609455877827435 | -0.0578840808367812 | 0.0293116133809418 | not significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | -0.0001666666666666 | 0.0025398065445916 | -0.0019835348181712 | 0.0016502014848378 | not significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.059030583613917 | 0.108852576458599 | -0.0188378586885034 | 0.1368990259163374 | not significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.3012043330751927 | 0.050792115195809 | 0.2648698427009843 | 0.337538823449401 | significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.3011377622893388 | 0.0508153980924356 | -0.3374889082444401 | -0.2647866163342376 | significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | -0.005 | 0.0075359222034725 | -0.010390873991116 | 0.0003908739911159 | not significant |
| 42 | merged_scans | centralized | order_2 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.4731904361071027 | 0.0846235745863599 | 0.4126543776187785 | 0.533726494595427 | significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.3012043330751927 | 0.050792115195809 | -0.337538823449401 | -0.2648698427009843 | significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.3011377622893388 | 0.0508153980924356 | 0.2647866163342376 | 0.3374889082444401 | significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.005 | 0.0075359222034725 | -0.0003908739911159 | 0.010390873991116 | not significant |
| 42 | merged_scans | centralized | order_2 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.4731904361071027 | 0.0846235745863599 | -0.533726494595427 | -0.4126543776187785 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0350630670827394 | 0.0267494428819665 | 0.0159276683862416 | 0.0541984657792372 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0366407489797044 | 0.0320915950306185 | -0.0595976931084894 | -0.0136838048509193 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1046666666666666 | 0.0919936927521275 | 0.0388583432506365 | 0.1704749900826967 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0141189774731441 | 0.0179917860221952 | 0.00124842909141 | 0.0269895258548782 | significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0083919373562435 | 0.0279636534614036 | -0.0116120552635579 | 0.0283959299760449 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0124258459744534 | 0.0307206327586577 | -0.0344020627741653 | 0.0095503708252584 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | 0.0344999999999999 | 0.0919945315068264 | -0.0313089234249964 | 0.1003089234249964 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0044393237934904 | 0.0200142870730211 | -0.0098780346822859 | 0.0187566822692669 | not significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.0352717078152615 | 0.0315012799081911 | 0.0127370496860042 | 0.0578063659445188 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.0386264483839085 | 0.0363014413697147 | -0.0645949351644437 | -0.0126579616033732 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | rare_random_60 | slowloris_recall | better | 10 | 0.1149999999999999 | 0.1059641215776754 | 0.0391978338442345 | 0.1908021661557654 | significant |
| 42 | merged_scans | centralized | order_3 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.1071918390251723 | 0.0130439382179517 | 0.0978607677398985 | 0.1165229103104461 | significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | -0.000208640732522 | 0.0227948735320579 | -0.0165151109344206 | 0.0160978294693764 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0019856994042041 | 0.025821172002413 | -0.016485654307993 | 0.0204570531164012 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | -0.0103333333333333 | 0.0811940215520974 | -0.0684160373742033 | 0.0477493707075366 | not significant |
| 42 | merged_scans | centralized | order_3 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.0930728615520282 | 0.0150190026349161 | -0.1038168088077156 | -0.0823289142963408 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0190074867087026 | 0.0213714855765536 | 0.0037192469106504 | 0.0342957265067548 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0189779050194794 | 0.0211706448242868 | -0.0341224719983971 | -0.0038333380405616 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0602222222222222 | 0.0630947422695236 | 0.0150869626092434 | 0.105357481835201 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0070370851370851 | 0.0103738162997868 | -0.0003838959942443 | 0.0144580662684146 | not significant |
| 42 | original_type | federated | averaged | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.001064464364247 | 0.0372076512279097 | -0.0276812146251012 | 0.0255522858966071 | not significant |
| 42 | original_type | federated | averaged | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0030628380273584 | 0.0379869384894612 | -0.024111380757782 | 0.0302370568124989 | not significant |
| 42 | original_type | federated | averaged | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | 0.0013888888888888 | 0.0293251134199324 | -0.0195890335144494 | 0.0223668112922272 | not significant |
| 42 | original_type | federated | averaged | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0063160173160173 | 0.0325385259335818 | -0.0169606419206944 | 0.0295926765527291 | not significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.0690288699077794 | 0.0428658997529566 | 0.0383644524888313 | 0.0996932873267275 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.0602746904115428 | 0.041265566595416 | -0.0897942984543895 | -0.0307550823686962 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.0883888888888888 | 0.0619617840980595 | -0.1327136790497342 | -0.0440640987280434 | significant |
| 42 | original_type | federated | averaged | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.2093549783549783 | 0.033657657043312 | 0.1852777409502338 | 0.2334322157597228 | significant |
| 42 | original_type | federated | averaged | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0500213831990768 | 0.0441007822459501 | -0.0815691823374507 | -0.0184735840607028 | significant |
| 42 | original_type | federated | averaged | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0412967853920634 | 0.0411813744896694 | 0.0118374047534908 | 0.070756166030636 | significant |
| 42 | original_type | federated | averaged | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.148611111111111 | 0.050383474602607 | 0.1125689446073099 | 0.1846532776149122 | significant |
| 42 | original_type | federated | averaged | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.2023178932178932 | 0.0347219472018178 | -0.2271564779374821 | -0.1774793084983043 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0396464505355885 | 0.038938669712589 | 0.0117914042473551 | 0.0675014968238219 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0396464505355885 | 0.038938669712589 | -0.0675014968238219 | -0.0117914042473551 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1211666666666666 | 0.1234660197167275 | 0.0328443968095253 | 0.209488936523808 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0176971139971139 | 0.0208419831421529 | 0.0027876574222388 | 0.032606570571989 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0102609719681198 | 0.080950002515239 | -0.047647171369545 | 0.0681691153057846 | not significant |
| 42 | original_type | federated | order_1 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0095329970495163 | 0.0811863839978312 | -0.0676102375131972 | 0.0485442434141645 | not significant |
| 42 | original_type | federated | order_1 | rare_random_60 | protected_60 | slowloris_recall | better | 10 | 0.0293333333333333 | 0.030012343139794 | 0.0078637964039033 | 0.0508028702627633 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0003571428571428 | 0.0856040774442542 | -0.0608803251219006 | 0.0615946108361863 | not significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.1231173530556446 | 0.1080208073616162 | 0.0458439225209243 | 0.200390783590365 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.1242203786042545 | 0.1080649571373891 | -0.201525391985971 | -0.046915365222538 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.1725 | 0.1296939655163571 | -0.2652774738949209 | -0.079722526105079 | significant |
| 42 | original_type | federated | order_1 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.2403152958152958 | 0.0953194128289421 | 0.1721278955749892 | 0.3085026960556024 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0834709025200561 | 0.0993525930610542 | -0.1545434660924308 | -0.0123983389476815 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.084573928068666 | 0.0992303512085553 | 0.0135888110496751 | 0.1555590450876569 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.2936666666666667 | 0.0918526732340813 | 0.2279592225367476 | 0.3593741107965857 | significant |
| 42 | original_type | federated | order_1 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.2226181818181818 | 0.089642218111564 | -0.2867443616108686 | -0.158492002025495 | significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | federated | order_2 | rare_random_60 | protected_60 | old_task_accuracy | worse | 10 | -0.0118863111701146 | 0.0153526747335374 | -0.0228689530658807 | -0.0009036692743486 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | protected_60 | forgetting | worse | 10 | 0.0139307556145591 | 0.0139617258621191 | 0.0039431385998151 | 0.0239183726293032 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | protected_60 | slowloris_recall | better | 10 | 0.0081666666666666 | 0.0053547025600095 | 0.0043361432109419 | 0.0119971901223913 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0220454545454545 | 0.0471825354072657 | -0.0117068979993651 | 0.0557978070902743 | not significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.1233996127890253 | 0.0297364115112579 | 0.1021274654556445 | 0.1446717601224061 | significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.1236218350112476 | 0.0293452513824646 | -0.1446141632451555 | -0.1026295067773396 | significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | 0.0018333333333333 | 0.0037226367928335 | -0.0008296806048427 | 0.0044963472715094 | not significant |
| 42 | original_type | federated | order_2 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.3653542568542568 | 0.0398948210756011 | 0.3368152210853388 | 0.3938932926231748 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.1233996127890253 | 0.0297364115112579 | -0.1446717601224061 | -0.1021274654556445 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.1236218350112476 | 0.0293452513824646 | 0.1026295067773396 | 0.1446141632451555 | significant |
| 42 | original_type | federated | order_2 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | -0.0018333333333333 | 0.0037226367928335 | -0.0044963472715094 | 0.0008296806048427 | not significant |
| 42 | original_type | federated | order_2 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.3653542568542568 | 0.0398948210756011 | -0.3938932926231748 | -0.3368152210853388 | significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0173760095905194 | 0.0330712976855049 | -0.0062817715982369 | 0.0410337907792758 | not significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0172872645228497 | 0.0324493969573889 | -0.0405001647309197 | 0.0059256356852203 | not significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0595 | 0.0900207452085419 | -0.0048969617656072 | 0.1238969617656072 | not significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0034141414141414 | 0.0240997390919301 | -0.0138257733773756 | 0.0206540562056585 | not significant |
| 42 | original_type | federated | order_3 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.0015680538907464 | 0.0347712726934083 | -0.026441923941385 | 0.0233058161598921 | not significant |
| 42 | original_type | federated | order_3 | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0047907555170326 | 0.039661766683748 | -0.0235815631832062 | 0.0331630742172715 | not significant |
| 42 | original_type | federated | order_3 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | -0.0333333333333333 | 0.0816987843117918 | -0.0917771229002278 | 0.0251104562335611 | not significant |
| 42 | original_type | federated | order_3 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | -0.0034545454545454 | 0.0254220585089083 | -0.0216403905728977 | 0.0147312996638069 | not significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | rare_random_60 | old_task_accuracy | worse | 10 | -0.0394303561213316 | 0.0412839079555164 | -0.068963084782791 | -0.0098976274598721 | significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | rare_random_60 | forgetting | worse | 10 | 0.0670181423808734 | 0.0451987603227861 | 0.0346848970426298 | 0.099351387719117 | significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.0944999999999999 | 0.118300856263142 | -0.1791273345101487 | -0.0098726654898512 | significant |
| 42 | original_type | federated | order_3 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.0223953823953823 | 0.0205499016013262 | 0.0076948683678443 | 0.0370958964229203 | significant |
| 42 | original_type | federated | order_3 | rare_random_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.056806365711851 | 0.0424142983729678 | 0.026465004458824 | 0.087147726964878 | significant |
| 42 | original_type | federated | order_3 | rare_random_60 | class_balanced_60 | forgetting | better | 10 | -0.0843054069037232 | 0.0388382247862187 | -0.1120885992202079 | -0.0565222145872385 | significant |
| 42 | original_type | federated | order_3 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1539999999999999 | 0.1193454370025655 | 0.06862541744406 | 0.2393745825559398 | significant |
| 42 | original_type | federated | order_3 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.0189812409812409 | 0.0207796134812267 | -0.0338460809884494 | -0.0041164009740324 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0082879881293905 | 0.0109244370782242 | 0.0004731166216346 | 0.0161028596371464 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0093138820950455 | 0.0102997781924329 | -0.0166818995549743 | -0.0019458646351167 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0371666666666666 | 0.023410293422647 | 0.0204199515959631 | 0.0539133817373701 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0033900913900913 | 0.0033793828248893 | 0.0009726265483861 | 0.0058075562317966 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.00528925616787 | 0.0254357493991492 | -0.0234848951591051 | 0.012906382823365 | not significant |
| 42 | original_type | centralized | averaged | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0015553155893891 | 0.0262441555656521 | -0.0172186223358834 | 0.0203292535146618 | not significant |
| 42 | original_type | centralized | averaged | rare_random_60 | protected_60 | slowloris_recall | worse | 10 | -0.0569999999999999 | 0.0433635538812563 | -0.0880204177364123 | -0.0259795822635876 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0206607503607503 | 0.0326435077086605 | -0.0026910083137651 | 0.0440125090352658 | not significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.0410813492415429 | 0.0223531856253193 | 0.0250908435340138 | 0.057071854949072 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.0447732907020298 | 0.0236701840029819 | -0.0617059202941727 | -0.0278406611098869 | significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | -0.0028333333333333 | 0.034328208894813 | -0.0273902546358609 | 0.0217235879691942 | not significant |
| 42 | original_type | centralized | averaged | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.1405888407888408 | 0.0220963183941591 | 0.1247820868290398 | 0.1563955947486417 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0327933611121524 | 0.0294173154303577 | -0.0538372408603929 | -0.0117494813639119 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0354594086069843 | 0.0288862473760439 | 0.0147954320589378 | 0.0561233851550307 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.04 | 0.0340146422114603 | 0.0156673907898912 | 0.0643326092101088 | significant |
| 42 | original_type | centralized | averaged | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.1371987493987493 | 0.0241061255145139 | -0.1544432327617662 | -0.1199542660357324 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0173368855254411 | 0.017364862709553 | 0.00491481106492 | 0.0297589599859622 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0173368855254411 | 0.017364862709553 | -0.0297589599859623 | -0.00491481106492 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0501666666666666 | 0.0510654989712739 | 0.0136366093206989 | 0.0866967240126343 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0027900432900432 | 0.0073358227255904 | -0.0024576881576885 | 0.008037774737775 | not significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.0109961333761231 | 0.0245091814197151 | -0.0285289455644181 | 0.0065366788121719 | not significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0112837758144459 | 0.0250413829562682 | -0.0066297504183908 | 0.0291973020472828 | not significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | protected_60 | slowloris_recall | worse | 10 | -0.1021666666666667 | 0.0539893107847502 | -0.1407882929851649 | -0.0635450403481684 | significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | protected_60 | worst_client_macro_recall | better | 10 | 0.0309209235209235 | 0.0407598832474324 | 0.0017630595532916 | 0.0600787874885554 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | rare_random_60 | old_task_accuracy | not significant | 10 | -0.016897630165213 | 0.0240153795849393 | -0.0340771978008199 | 0.0002819374703938 | not significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | rare_random_60 | forgetting | not significant | 10 | 0.0139766422332122 | 0.0247483848929546 | -0.003727285811597 | 0.0316805702780214 | not significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | rare_random_60 | slowloris_recall | worse | 10 | -0.0881666666666666 | 0.0637096519617429 | -0.1337418061745231 | -0.0425915271588102 | significant |
| 42 | original_type | centralized | order_1 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.0405507936507936 | 0.0326039463155362 | 0.0172273354920594 | 0.0638742518095278 | significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0342345156906542 | 0.0208077451173509 | 0.019349551523268 | 0.0491194798580403 | significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | class_balanced_60 | forgetting | better | 10 | -0.0313135277586534 | 0.0220120184727976 | -0.0470599771875355 | -0.0155670783297712 | significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1383333333333333 | 0.0535700764085674 | 0.100011609221058 | 0.1766550574456086 | significant |
| 42 | original_type | centralized | order_1 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.0377607503607503 | 0.0337884709881257 | -0.0619315664243147 | -0.013589934297186 | significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | 0.0147419810451008 | 0.0638167496048702 | -0.0309097715013799 | 0.0603937335915816 | not significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | protected_60 | forgetting | not significant | 10 | -0.0166975366006563 | 0.0639461324234247 | -0.0624418440399041 | 0.0290467708385914 | not significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | -0.0005 | 0.0022291558497487 | -0.0020946420316039 | 0.0010946420316039 | not significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | 0.0332034632034632 | 0.0720958634740205 | -0.0183708106246364 | 0.0847777370315629 | not significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.098838289633809 | 0.0590887615393079 | 0.0565687360013777 | 0.1411078432662403 | significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.0991939410701774 | 0.0587491437048909 | -0.1412205467393675 | -0.0571673354009873 | significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | rare_random_60 | slowloris_recall | not significant | 10 | -0.0036666666666666 | 0.0068403306540539 | -0.0085599444391708 | 0.0012266111058375 | not significant |
| 42 | original_type | centralized | order_2 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.3188311688311688 | 0.0590658626863269 | 0.2765779960513563 | 0.3610843416109813 | significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.098838289633809 | 0.0590887615393079 | -0.1411078432662403 | -0.0565687360013777 | significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0991939410701774 | 0.0587491437048909 | 0.0571673354009873 | 0.1412205467393675 | significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0036666666666666 | 0.0068403306540539 | -0.0012266111058375 | 0.0085599444391708 | not significant |
| 42 | original_type | centralized | order_2 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.3188311688311688 | 0.0590658626863269 | -0.3610843416109813 | -0.2765779960513563 | significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0075270788627304 | 0.0320643555472607 | -0.0154103793135195 | 0.0304645370389803 | not significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0106047607596954 | 0.0288878995116989 | -0.0312699191743922 | 0.0100603976550014 | not significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0613333333333333 | 0.0640399181066865 | 0.015521935657883 | 0.1071447310087836 | significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0073802308802308 | 0.0103921756593383 | -5.388374574297888e-05 | 0.0148143455062047 | not significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | protected_60 | old_task_accuracy | not significant | 10 | -0.0196136161725879 | 0.0326127707851665 | -0.0429433869766136 | 0.0037161546314378 | not significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | protected_60 | forgetting | not significant | 10 | 0.0100797075543779 | 0.038087969331636 | -0.0171667843414283 | 0.0373261994501842 | not significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | protected_60 | slowloris_recall | not significant | 10 | -0.0683333333333333 | 0.1019803902718557 | -0.1412857097879468 | 0.0046190431212801 | not significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | protected_60 | worst_client_macro_recall | not significant | 10 | -0.0021421356421356 | 0.0224295309100855 | -0.0181872554763605 | 0.0139029841920892 | not significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | rare_random_60 | old_task_accuracy | better | 10 | 0.0413033882560328 | 0.0194025209619231 | 0.0274236608926695 | 0.0551831156193961 | significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | rare_random_60 | forgetting | better | 10 | -0.0491025732691243 | 0.0237004404534857 | -0.0660568470220853 | -0.0321482995161633 | significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | rare_random_60 | slowloris_recall | better | 10 | 0.0833333333333333 | 0.0639540730273696 | 0.0375833455282159 | 0.1290833211384507 | significant |
| 42 | original_type | centralized | order_3 | balanced_rare_60 | rare_random_60 | worst_client_macro_recall | better | 10 | 0.0623845598845598 | 0.0174738604710638 | 0.0498845131226066 | 0.074884606646513 | significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0337763093933024 | 0.0335431667858474 | -0.0577716454017033 | -0.0097809733849015 | significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | class_balanced_60 | forgetting | worse | 10 | 0.0384978125094288 | 0.0340685524100413 | 0.0141266382664629 | 0.0628689867523948 | significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | class_balanced_60 | slowloris_recall | not significant | 10 | -0.0219999999999999 | 0.0741195230941464 | -0.0750219127126918 | 0.0310219127126919 | not significant |
| 42 | original_type | centralized | order_3 | rare_random_60 | class_balanced_60 | worst_client_macro_recall | worse | 10 | -0.0550043290043289 | 0.018998331439192 | -0.0685949166012854 | -0.0414137414073725 | significant |
| 43 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0223096951878052 | 0.0178392069897254 | 0.0095482952706548 | 0.0350710951049555 | significant |
| 43 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0236912086295576 | 0.0188023742612677 | -0.0371416169060112 | -0.0102408003531039 | significant |
| 43 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0792777777777778 | 0.0544860322393791 | 0.0403008183363667 | 0.1182547372191889 | significant |
| 43 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0064386676286676 | 0.0176758652464021 | -0.006205884644363 | 0.0190832199016983 | not significant |
| 43 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0471181818181817 | 0.0415561141973594 | 0.0173907285417715 | 0.076845635094592 | significant |
| 43 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.047107118647477 | 0.0415651134587977 | -0.0768410096077058 | -0.0173732276872482 | significant |
| 43 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1471666666666667 | 0.1245957661330095 | 0.0580362249086417 | 0.2362971084246916 | significant |
| 43 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0096911880711881 | 0.0479321392121079 | -0.0245973987321678 | 0.043979774874544 | not significant |
| 43 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0198109037452337 | 0.0322967509953528 | -0.0032928001197251 | 0.0429146076101927 | not significant |
| 43 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0239665072411957 | 0.0355701391802956 | -0.049411851950178 | 0.0014788374677866 | not significant |
| 43 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0906666666666666 | 0.10301084684586 | 0.0169771459855357 | 0.1643561873477975 | significant |
| 43 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0096248148148148 | 0.0316839444836227 | -0.0130405136799538 | 0.0322901433095834 | not significant |
| 43 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0110754390397452 | 0.0089010476215589 | 0.0047080131532842 | 0.0174428649262062 | significant |
| 43 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0113109323428697 | 0.009407660066779 | -0.0180407669406698 | -0.0045810977450695 | significant |
| 43 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0347777777777777 | 0.0303389629832187 | 0.0130745910877266 | 0.0564809644678289 | significant |
| 43 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0138991769547325 | 0.0321321421591334 | -0.0090867728424529 | 0.036885126751918 | not significant |
| 43 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0255009722180316 | 0.015269880766393 | 0.0145775575584351 | 0.0364243868776282 | significant |
| 43 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0232634870870244 | 0.0149740120879315 | -0.033975250044223 | -0.0125517241298259 | significant |
| 43 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0748333333333333 | 0.0469136980180457 | 0.0412732954714753 | 0.1083933711951913 | significant |
| 43 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0137962962962962 | 0.0565194258895774 | -0.0266352653353422 | 0.0542278579279347 | not significant |
| 43 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.007725344901204 | 0.0292867763150971 | -0.0132251527894354 | 0.0286758425918435 | not significant |
| 43 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0106693099415846 | 0.0309134002592784 | -0.0327834243041123 | 0.0114448044209431 | not significant |
| 43 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0294999999999999 | 0.0941959148284593 | -0.0378836981868164 | 0.0968836981868164 | not significant |
| 43 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0279012345679012 | 0.0513264583269838 | -0.0088155018553513 | 0.0646179709911537 | not significant |
| 43 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0460796689907452 | 0.0188980016147661 | 0.0325608530265667 | 0.0595984849549237 | significant |
| 43 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0557389602102754 | 0.0196674831022445 | -0.0698082300705385 | -0.0416696903500123 | significant |
| 43 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1076666666666666 | 0.0503157383467363 | 0.0716729557612873 | 0.143660377572046 | significant |
| 43 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0070585927300212 | 0.0134004086439441 | -0.0025274821362607 | 0.0166446675963033 | not significant |
| 43 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0483505968778696 | 0.0422151380767934 | 0.0181517063181062 | 0.0785494874376329 | significant |
| 43 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0483395337071648 | 0.0422241615822747 | -0.0785448792938902 | -0.0181341881204394 | significant |
| 43 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1475 | 0.1247967483352901 | 0.0582257842355963 | 0.2367742157644037 | significant |
| 43 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.010818635332921 | 0.0308032126400128 | -0.0112166555552124 | 0.0328539262210546 | not significant |
| 43 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0898884100943661 | 0.0471830977280742 | 0.0561356552894726 | 0.1236411648992595 | significant |
| 43 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.1188773469236613 | 0.0491928836238168 | -0.1540678159485978 | -0.0836868778987248 | significant |
| 43 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1755 | 0.1111945520026126 | 0.0959562093185537 | 0.2550437906814462 | significant |
| 43 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0103571428571428 | 0.0284833850690837 | -0.010018643357464 | 0.0307329290717497 | not significant |
| 43 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0050245972889034 | 0.0061359197732149 | 0.0006352247046487 | 0.0094139698731582 | significant |
| 43 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0061105650334114 | 0.0084308538035271 | -0.0121416345249984 | -7.949554182451121e-05 | significant |
| 43 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0249444444444444 | 0.0163476673476429 | 0.0132500277107876 | 0.0366388611781012 | significant |
| 43 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.008531746031746 | 0.0201850724996334 | -0.0059077849783967 | 0.0229712770418888 | not significant |
| 43 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0207874256550357 | 0.0153889529249583 | 0.0097788319045005 | 0.0317960194055708 | significant |
| 43 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0190458082926236 | 0.0149281494195818 | -0.0297247630732919 | -0.0083668535119552 | significant |
| 43 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0716666666666666 | 0.0473103752356528 | 0.037822863017752 | 0.1055104703155812 | significant |
| 43 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0069047619047619 | 0.0359244258673358 | -0.0187940242324883 | 0.0326035480420121 | not significant |
| 43 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 43 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | -0.0057136337883252 | 0.0141913975464105 | -0.0158655480285332 | 0.0044382804518827 | not significant |
| 43 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0007141131923891 | 0.023906810632459 | -0.0163877888932869 | 0.0178160152780652 | not significant |
| 43 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0031666666666666 | 0.0459028092956691 | -0.0296702249664707 | 0.036003558299804 | not significant |
| 43 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0186904761904762 | 0.0347717334079348 | -0.0061837234354805 | 0.0435646758164329 | not significant |
| 44 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.033727852268778 | 0.0176007858469495 | 0.0211370085626419 | 0.046318695974914 | significant |
| 44 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0348427310041346 | 0.0178746039744844 | -0.0476294523987828 | -0.0220560096094863 | significant |
| 44 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1127777777777777 | 0.0516118785574644 | 0.075856864021547 | 0.1496986915340085 | significant |
| 44 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0138987093153759 | 0.0153289155434832 | 0.0029330637202954 | 0.0248643549104565 | significant |
| 44 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0735436713939625 | 0.0566722496430842 | 0.0330027862348565 | 0.1140845565530686 | significant |
| 44 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0735436713939625 | 0.0566722496430843 | -0.1140845565530686 | -0.0330027862348564 | significant |
| 44 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.2269999999999999 | 0.1739053950277365 | 0.1025955746812534 | 0.3514044253187465 | significant |
| 44 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.028240891053391 | 0.023014473715898 | 0.0117773283434299 | 0.0447044537633521 | significant |
| 44 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0276398854123713 | 0.0415417919040501 | -0.0020773223126107 | 0.0573570931373534 | not significant |
| 44 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0309845216184413 | 0.0475396416041209 | -0.0649923325473465 | 0.0030232893104639 | not significant |
| 44 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1113333333333333 | 0.1474051274716666 | 0.0058860574209068 | 0.2167806092457598 | significant |
| 44 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0134552368927368 | 0.0354289767888194 | -0.0118891263246396 | 0.0387996001101133 | not significant |
| 44 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.011326774925227 | 0.0185410393581717 | -0.0019366856235255 | 0.0245902354739796 | not significant |
| 44 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0115562127932311 | 0.0193506355902984 | -0.0253988235976838 | 0.0022863980112215 | not significant |
| 44 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0379999999999999 | 0.0642137206556274 | -0.0079357285291106 | 0.0839357285291106 | not significant |
| 44 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0006180820105819 | 0.0085905934918344 | -0.0067634223913573 | 0.0055272583701933 | not significant |
| 44 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0157630314550629 | 0.0279456950404907 | -0.0042281144843181 | 0.0357541773944439 | not significant |
| 44 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0158183473085865 | 0.0279555929622134 | -0.0358165737946267 | 0.0041798791774536 | not significant |
| 44 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0509999999999999 | 0.086324824405509 | -0.0107530592952349 | 0.1127530592952348 | not significant |
| 44 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0116849037999038 | 0.0281451567405116 | -0.0318187360438716 | 0.0084489284440639 | not significant |
| 44 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0182172933206183 | 0.0310669870944234 | -0.0040066904450966 | 0.0404412770863332 | not significant |
| 44 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0188502910711069 | 0.0343664530908966 | -0.0434345706234162 | 0.0057339884812023 | not significant |
| 44 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.063 | 0.1186779020898349 | -0.0218970568461411 | 0.1478970568461411 | not significant |
| 44 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0098306577681577 | 0.0176633633977089 | -0.0028049512210727 | 0.0224662667573883 | not significant |
| 44 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0345478544204579 | 0.021315528346791 | 0.0192996440131554 | 0.0497960648277605 | significant |
| 44 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0357738442669257 | 0.0211014904192242 | -0.0508689411646036 | -0.0206787473692478 | significant |
| 44 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1134444444444444 | 0.04438715443389 | 0.0816917869837496 | 0.1451971019051392 | significant |
| 44 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0062481962481962 | 0.0117977247463476 | -0.0021913876238512 | 0.0146877801202437 | not significant |
| 44 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0727574454986457 | 0.0605318752522109 | 0.0294555505055874 | 0.1160593404917039 | significant |
| 44 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0727574454986457 | 0.060531875252211 | -0.116059340491704 | -0.0294555505055874 | significant |
| 44 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.2219999999999999 | 0.1832740644937231 | 0.0908936322789981 | 0.3531063677210018 | significant |
| 44 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0159848484848485 | 0.0132427374236532 | 0.0065115648148744 | 0.0254581321548225 | significant |
| 44 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0308861177627281 | 0.0520166460531493 | -0.0063243492168534 | 0.0680965847423098 | not significant |
| 44 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0345640873021315 | 0.0501582985320546 | -0.0704451725488035 | 0.0013169979445404 | not significant |
| 44 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1183333333333333 | 0.095565244986777 | 0.0499700753612096 | 0.1866965913054569 | significant |
| 44 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0027597402597402 | 0.0323121690740928 | -0.020354993034322 | 0.0258744735538026 | not significant |
| 44 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0089743108909448 | 0.0140962547210527 | -0.0011095422720897 | 0.0190581640539795 | not significant |
| 44 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0088000290751097 | 0.0128582110028761 | -0.0179982391144525 | 0.0003981809642329 | not significant |
| 44 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0315555555555555 | 0.036976617384452 | 0.0051040769501318 | 0.0580070341609791 | significant |
| 44 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0011847522847522 | 0.0076905618707531 | -0.0066862488297945 | 0.00431674426029 | not significant |
| 44 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0122933344853659 | 0.026085661835718 | -0.0063672238556451 | 0.030953892826377 | not significant |
| 44 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0123486503388896 | 0.0260803113732454 | -0.0310053811896207 | 0.0063080805118415 | not significant |
| 44 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0399999999999999 | 0.078751837133186 | -0.0163356705511463 | 0.0963356705511463 | not significant |
| 44 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0066155844155843 | 0.021607833075652 | -0.0220728970293256 | 0.0088417281981568 | not significant |
| 44 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 44 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0146295981874686 | 0.0251295119881965 | -0.0033469717569746 | 0.0326061681319119 | not significant |
| 44 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0140514368864397 | 0.0280871047682658 | -0.0341437412511562 | 0.0060408674782767 | not significant |
| 44 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0546666666666666 | 0.0564527552936693 | 0.0142827983062362 | 0.0950505350270971 | significant |
| 44 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0030613275613275 | 0.0102824144865149 | -0.0042942686516595 | 0.0104169237743146 | not significant |
| 45 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.020593212130152 | 0.0232241667325315 | 0.0039796440726082 | 0.0372067801876957 | significant |
| 45 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0203006834581013 | 0.023682234126304 | -0.0372419331891805 | -0.003359433727022 | significant |
| 45 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.0608888888888888 | 0.0669644583576061 | 0.0129854011481523 | 0.1087923766296254 | significant |
| 45 | merged_scans | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.009268683662017 | 0.0184975323472502 | -0.0039636538460146 | 0.0225010211700487 | not significant |
| 45 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0530399029671545 | 0.0472648032942737 | 0.0192286995212239 | 0.0868511064130851 | significant |
| 45 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0530399029671545 | 0.0472648032942737 | -0.0868511064130851 | -0.019228699521224 | significant |
| 45 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1611666666666666 | 0.1406994213225265 | 0.0605163639574412 | 0.261816969375892 | significant |
| 45 | merged_scans | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0335845695045695 | 0.0247364476023733 | 0.0158891808830162 | 0.0512799581261228 | significant |
| 45 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0087397334233015 | 0.0319753570013345 | -0.0141340590284987 | 0.0316135258751018 | not significant |
| 45 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0078621474071493 | 0.0333417437111719 | -0.0317133940280591 | 0.0159890992137603 | not significant |
| 45 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0215 | 0.0863757582018141 | -0.040289495138169 | 0.083289495138169 | not significant |
| 45 | merged_scans | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0057785185185185 | 0.0341638112999745 | -0.0302178368662532 | 0.0186607998292162 | not significant |
| 45 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0081863032765576 | 0.0113371979050092 | 7.616046084671368e-05 | 0.0162964460922686 | significant |
| 45 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0085562741435414 | 0.0128859082543043 | -0.0177742976029697 | 0.0006617493158868 | not significant |
| 45 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0260555555555555 | 0.0365912524121055 | -0.0001202495555806 | 0.0522313606666918 | not significant |
| 45 | merged_scans | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0016744936133824 | 0.0107529723644287 | -0.0093667066539943 | 0.0060177194272294 | not significant |
| 45 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0136585964646007 | 0.0210003676214686 | -0.0013641615413514 | 0.028681354470553 | not significant |
| 45 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0136585964646007 | 0.0210003676214686 | -0.028681354470553 | 0.0013641615413514 | not significant |
| 45 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0366666666666666 | 0.0544727817411345 | -0.0023008139393175 | 0.0756341472726509 | not significant |
| 45 | merged_scans | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0054697771364437 | 0.0302874529425159 | -0.0271361157631512 | 0.0161965614902637 | not significant |
| 45 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0109003133650721 | 0.0308572665109098 | -0.011173645332902 | 0.0329742720630463 | not significant |
| 45 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0120102259660235 | 0.0359731262631766 | -0.0377438502677621 | 0.0137233983357149 | not significant |
| 45 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0415 | 0.1087540264615749 | -0.0362979438814657 | 0.1192979438814657 | not significant |
| 45 | merged_scans | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0004462962962963 | 0.0149622799199651 | -0.0102570739735254 | 0.0111496665661181 | not significant |
| 45 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.003719368300064 | 0.0214392124449277 | -0.0116173203809993 | 0.0190560569811274 | not significant |
| 45 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0043694566682829 | 0.0231288523341955 | -0.0121759275761727 | 0.0209148409127386 | not significant |
| 45 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0365555555555555 | 0.0574747514196839 | -0.0045594047914952 | 0.0776705159026063 | not significant |
| 45 | original_type | federated | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0060315055315055 | 0.009073795486222 | -0.000459496732934 | 0.012522507795945 | not significant |
| 45 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | better | 10 | 0.0541167624712868 | 0.0470097106180532 | 0.0204880413329532 | 0.0877454836096203 | significant |
| 45 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | better | 10 | -0.0541167624712868 | 0.0470097106180531 | -0.0877454836096203 | -0.0204880413329532 | significant |
| 45 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | better | 10 | 0.1615 | 0.1407880159392082 | 0.0607863205198994 | 0.2622136794801006 | significant |
| 45 | original_type | federated | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | better | 10 | 0.0156534116676973 | 0.0121162798009019 | 0.0069859472374423 | 0.0243208760979523 | significant |
| 45 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | federated | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | worse | 10 | -0.0429586575710945 | 0.0206072832605087 | -0.0577002199648048 | -0.0282170951773843 | significant |
| 45 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | worse | 10 | 0.0672251324761357 | 0.0234145197870438 | 0.0504753940464738 | 0.0839748709057976 | significant |
| 45 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | worse | 10 | -0.0518333333333333 | 0.062723427800637 | -0.096702970576707 | -0.0069636960899596 | significant |
| 45 | original_type | federated | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0024411049268191 | 0.0203818601032982 | -0.0121391994546147 | 0.0170214093082531 | not significant |
| 45 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0060683170397921 | 0.0125222267728389 | -0.002889544360296 | 0.0150261784398803 | not significant |
| 45 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0053642138327019 | 0.0152634087554956 | -0.0162829986946074 | 0.0055545710292036 | not significant |
| 45 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0123888888888888 | 0.0228297359816783 | -0.0039425204071046 | 0.0287202981848824 | not significant |
| 45 | original_type | centralized | averaged | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0028988868274582 | 0.006893824862643 | -0.007830432051506 | 0.0020326583965896 | not significant |
| 45 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0132094208841576 | 0.0193220697161002 | -0.0006127551249122 | 0.0270315968932275 | not significant |
| 45 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.0132094208841576 | 0.0193220697161002 | -0.0270315968932275 | 0.0006127551249122 | not significant |
| 45 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0343333333333333 | 0.053548178376182 | -0.0039727258702478 | 0.0726393925369145 | not significant |
| 45 | original_type | centralized | order_1 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0053308596165739 | 0.0194954711125354 | -0.0192770795120887 | 0.0086153602789409 | not significant |
| 45 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | centralized | order_2 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | 0.0 | 0.0 | 0.0 | 0.0 | not significant |
| 45 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | old_task_accuracy | not significant | 10 | 0.0049955302352188 | 0.0331465618488333 | -0.0187160916925466 | 0.0287071521629843 | not significant |
| 45 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | forgetting | not significant | 10 | -0.002883220613948 | 0.0426103297513697 | -0.0333648142673018 | 0.0275983730394057 | not significant |
| 45 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | slowloris_recall | not significant | 10 | 0.0028333333333333 | 0.0821322706160204 | -0.055920553654935 | 0.0615872203216016 | not significant |
| 45 | original_type | centralized | order_3 | balanced_rare_60 | class_balanced_60 | worst_client_macro_recall | not significant | 10 | -0.0033658008658008 | 0.0090942128855883 | -0.009871408857879 | 0.0031398071262773 | not significant |

## per_order_summary.csv

| split_seed | score_space | environment | method | order | old_task_accuracy_mean | old_task_accuracy_std | forgetting_mean | forgetting_std | slowloris_recall_mean | slowloris_recall_std | worst_client_macro_recall_mean | worst_client_macro_recall_std |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | merged_scans | centralized | balanced_rare_60 | order_1 | 0.9118072135835013 | 0.0082533405166417 | 0.0826776586734495 | 0.0093721482835053 | 0.7568333333333334 | 0.022353086897052 | 0.8382966570466571 | 0.0348159396255235 |
| 42 | merged_scans | centralized | balanced_rare_60 | order_2 | 0.8866325773500019 | 0.0095586642525929 | 0.1123938636279823 | 0.0095111065806813 | 0.9941666666666666 | 0.006815468970214 | 0.859263468013468 | 0.0103590508039059 |
| 42 | merged_scans | centralized | balanced_rare_60 | order_3 | 0.9524114376422708 | 0.0176124006566784 | 0.0361577571570028 | 0.0207908568022859 | 0.8998333333333333 | 0.0589802750036499 | 0.8680166847041846 | 0.0137943298778146 |
| 42 | merged_scans | centralized | class_balanced_60 | order_1 | 0.8967791873720155 | 0.0135425881789154 | 0.0977056848849353 | 0.0143183458299975 | 0.7115 | 0.0412568737258366 | 0.8331725889850891 | 0.0326197601603239 |
| 42 | merged_scans | centralized | class_balanced_60 | order_2 | 0.8866325773500019 | 0.0095586642525929 | 0.1123938636279823 | 0.0095111065806813 | 0.9941666666666666 | 0.006815468970214 | 0.859263468013468 | 0.0103590508039059 |
| 42 | merged_scans | centralized | class_balanced_60 | order_3 | 0.9173483705595312 | 0.0215338888876091 | 0.0727985061367072 | 0.0266097703139981 | 0.7951666666666666 | 0.0812648846764793 | 0.8538977072310405 | 0.0151420375948064 |
| 42 | merged_scans | centralized | protected_60 | order_1 | 0.9345170469136346 | 0.022105268654213 | 0.0633725206992533 | 0.0224350666653425 | 0.9615 | 0.0159174180547871 | 0.7246735746352413 | 0.0539995307943234 |
| 42 | merged_scans | centralized | protected_60 | order_2 | 0.5711864549913338 | 0.0367750064866835 | 0.427817859645241 | 0.036823130681283 | 0.9993333333333334 | 0.0014054567378525 | 0.3270424482924482 | 0.0896649407646864 |
| 42 | merged_scans | centralized | protected_60 | order_3 | 0.9087477924707656 | 0.0143068729130839 | 0.0872100515153648 | 0.0153233268800307 | 0.7503333333333333 | 0.0501097560792405 | 0.7563855218855219 | 0.0102948792175043 |
| 42 | merged_scans | centralized | rare_random_60 | order_1 | 0.9267333541186844 | 0.0143453056457303 | 0.0714438559325262 | 0.0143359374137387 | 0.8588333333333333 | 0.0491850248212468 | 0.7653846464646465 | 0.0294183069646177 |
| 42 | merged_scans | centralized | rare_random_60 | order_2 | 0.5854282442748092 | 0.0493753722861062 | 0.4135316259173212 | 0.0493923167652278 | 0.9991666666666668 | 0.0018002057495577 | 0.3860730319063652 | 0.0835575928947585 |
| 42 | merged_scans | centralized | rare_random_60 | order_3 | 0.9171397298270092 | 0.0269100609561984 | 0.0747842055409113 | 0.0296532807124233 | 0.7848333333333334 | 0.0896820515508559 | 0.7608248456790123 | 0.0140578495710024 |
| 42 | merged_scans | federated | balanced_rare_60 | order_1 | 0.8682656684821847 | 0.0383074392120073 | 0.1287315126950645 | 0.0383910904650593 | 0.6256666666666667 | 0.1199310501501736 | 0.8055508658008659 | 0.0269548643609894 |
| 42 | merged_scans | federated | balanced_rare_60 | order_2 | 0.8220528930191392 | 0.0125155322988951 | 0.1772280008850536 | 0.012487559830295 | 0.9986666666666666 | 0.0021942686286812 | 0.8169128787878787 | 0.0135057401155875 |
| 42 | merged_scans | federated | balanced_rare_60 | order_3 | 0.8753223154210541 | 0.0189582254780647 | 0.1211803214536823 | 0.0192944368896823 | 0.6741666666666666 | 0.0211001433498143 | 0.7483655303030303 | 0.0280893100053948 |
| 42 | merged_scans | federated | class_balanced_60 | order_1 | 0.8324494291495348 | 0.0279070981919236 | 0.1645477520277145 | 0.027434058408778 | 0.5096666666666667 | 0.0867656130326886 | 0.7761566666666666 | 0.0279414028301757 |
| 42 | merged_scans | federated | class_balanced_60 | order_2 | 0.8220528930191392 | 0.0125155322988951 | 0.1772280008850536 | 0.012487559830295 | 0.9986666666666666 | 0.0021942686286812 | 0.8169128787878787 | 0.0135057401155875 |
| 42 | merged_scans | federated | class_balanced_60 | order_3 | 0.8651586667446878 | 0.0286093627098747 | 0.1314218917290455 | 0.0287214642824309 | 0.6385 | 0.0766120981323897 | 0.7459192424242425 | 0.0188910925502487 |
| 42 | merged_scans | federated | protected_60 | order_1 | 0.7334282066356471 | 0.0609487551439961 | 0.2641644108465398 | 0.0609523364220897 | 0.7741666666666667 | 0.0218898758942728 | 0.4565123456790123 | 0.1048561820856243 |
| 42 | merged_scans | federated | protected_60 | order_2 | 0.5593507025113398 | 0.0144895502891409 | 0.4399301913928531 | 0.0144725219781488 | 0.9685 | 0.0447175635944889 | 0.2303170594837261 | 0.0447491960971443 |
| 42 | merged_scans | federated | protected_60 | order_3 | 0.892361301668893 | 0.0193039404918744 | 0.100997513986682 | 0.0223987019369667 | 0.7391666666666666 | 0.0612636983926104 | 0.7277810746352413 | 0.0213643516564625 |
| 42 | merged_scans | federated | rare_random_60 | order_1 | 0.7373345413218569 | 0.0813162244580902 | 0.2609860510789334 | 0.0814006311289215 | 0.8031666666666666 | 0.0298602713060202 | 0.4557407407407408 | 0.134610069405227 |
| 42 | merged_scans | federated | rare_random_60 | order_2 | 0.5282533761109267 | 0.0134377854661554 | 0.4710275177932662 | 0.0134508742907147 | 0.9981666666666668 | 0.0037226367928335 | 0.2731112714446048 | 0.0639961679272193 |
| 42 | merged_scans | federated | rare_random_60 | order_3 | 0.8966368610218896 | 0.0131465235594284 | 0.0961113229266384 | 0.0162736140512975 | 0.742 | 0.065432087118564 | 0.7297166049382716 | 0.013011681930379 |
| 42 | original_type | centralized | balanced_rare_60 | order_1 | 0.5895565687652252 | 0.0118241154456824 | 0.1606774311317623 | 0.0118005617983497 | 0.7711666666666667 | 0.0302566184984865 | 0.5460440115440115 | 0.0157960528850066 |
| 42 | original_type | centralized | balanced_rare_60 | order_2 | 0.4131103551277796 | 0.0245645433539586 | 0.3206494191835379 | 0.0237187718000693 | 0.9955 | 0.0062385697949465 | 0.5568506493506493 | 0.0075223241013815 |
| 42 | original_type | centralized | balanced_rare_60 | order_3 | 0.6530583614255582 | 0.0092175271343897 | 0.3238441667070487 | 0.0141152078688623 | 0.9271666666666668 | 0.0199079672617228 | 0.5678455988455988 | 0.0066570537816887 |
| 42 | original_type | centralized | class_balanced_60 | order_1 | 0.572219683239784 | 0.0145388413394204 | 0.1780143166572035 | 0.0160950162674835 | 0.721 | 0.0424424083281257 | 0.5432539682539683 | 0.0164359180523064 |
| 42 | original_type | centralized | class_balanced_60 | order_2 | 0.4131103551277796 | 0.0245645433539586 | 0.3206494191835379 | 0.0237187718000693 | 0.9955 | 0.0062385697949465 | 0.5568506493506493 | 0.0075223241013815 |
| 42 | original_type | centralized | class_balanced_60 | order_3 | 0.6455312825628277 | 0.0367136149393437 | 0.3344489274667441 | 0.0365996424345922 | 0.8658333333333333 | 0.0518797874482828 | 0.5604653679653679 | 0.0065438265922052 |
| 42 | original_type | centralized | protected_60 | order_1 | 0.6174503323065614 | 0.0227700144723186 | 0.1354170130841041 | 0.0235260368314621 | 0.9615 | 0.0159174180547871 | 0.4745722943722944 | 0.0361652858798435 |
| 42 | original_type | centralized | protected_60 | order_2 | 0.2995300844488697 | 0.0382112196500474 | 0.4365408968543717 | 0.0401768814401004 | 0.9996666666666666 | 0.0010540925533894 | 0.2048160173160173 | 0.056699749447652 |
| 42 | original_type | centralized | protected_60 | order_3 | 0.6313685893421132 | 0.0202747266653869 | 0.3628670324217951 | 0.0208189443684098 | 0.9121666666666666 | 0.0624650519574696 | 0.5076031746031746 | 0.0129740697620617 |
| 42 | original_type | centralized | rare_random_60 | order_1 | 0.6064541989304383 | 0.0174077855943094 | 0.1467007888985501 | 0.0178551786026524 | 0.8593333333333334 | 0.0486560110100222 | 0.5054932178932179 | 0.024642373012866 |
| 42 | original_type | centralized | rare_random_60 | order_2 | 0.3142720654939706 | 0.049051905509809 | 0.4198433602537154 | 0.0493221374956079 | 0.9991666666666668 | 0.0018002057495577 | 0.2380194805194805 | 0.0544657078788962 |
| 42 | original_type | centralized | rare_random_60 | order_3 | 0.6117549731695252 | 0.0217203315100775 | 0.372946739976173 | 0.0250939280522612 | 0.8438333333333332 | 0.0659173163333626 | 0.505461038961039 | 0.0176850812875332 |
| 42 | original_type | federated | balanced_rare_60 | order_1 | 0.5417620872149672 | 0.0377772333899638 | 0.209033257414991 | 0.0378134876207071 | 0.631 | 0.1195934471139309 | 0.5355533910533911 | 0.0146794719696003 |
| 42 | original_type | federated | balanced_rare_60 | order_2 | 0.388030670796917 | 0.0290119105542575 | 0.3465946675517203 | 0.0285102418471398 | 1.0 | 0.0 | 0.5348997113997114 | 0.0108803119238319 |
| 42 | original_type | federated | balanced_rare_60 | order_3 | 0.5575145857086388 | 0.0258297192145673 | 0.4366547178327645 | 0.0264352472561692 | 0.7171666666666667 | 0.0590200321715505 | 0.5019191919191919 | 0.0211671266688291 |
| 42 | original_type | federated | class_balanced_60 | order_1 | 0.5021156366793786 | 0.0276423015135154 | 0.2486797079505796 | 0.0269698615611215 | 0.5098333333333334 | 0.0866112714701672 | 0.517856277056277 | 0.0180697144903956 |
| 42 | original_type | federated | class_balanced_60 | order_2 | 0.388030670796917 | 0.0290119105542575 | 0.3465946675517203 | 0.0285102418471398 | 1.0 | 0.0 | 0.5348997113997114 | 0.0108803119238319 |
| 42 | original_type | federated | class_balanced_60 | order_3 | 0.5401385761181193 | 0.0274160319602331 | 0.4539419823556142 | 0.0270655983895878 | 0.6576666666666667 | 0.0739669595908275 | 0.4985050505050504 | 0.0141308923499076 |
| 42 | original_type | federated | protected_60 | order_1 | 0.4083837621912026 | 0.0603170293025249 | 0.342786633068762 | 0.0600292799933706 | 0.7741666666666667 | 0.0218898758942728 | 0.2948809523809523 | 0.0671914577004121 |
| 42 | original_type | federated | protected_60 | order_2 | 0.2765173691780064 | 0.0102850260707071 | 0.4562857469484087 | 0.0095612956750766 | 0.99 | 0.0070710678118655 | 0.1474999999999999 | 0.0230121097087526 |
| 42 | original_type | federated | protected_60 | order_3 | 0.5985129957207168 | 0.0244503416334749 | 0.3648458199348583 | 0.0356144255746565 | 0.845 | 0.0666064542900041 | 0.4829783549783549 | 0.0219611814002249 |
| 42 | original_type | federated | rare_random_60 | order_1 | 0.4186447341593224 | 0.0811500046327137 | 0.3332536360192456 | 0.0808422338692532 | 0.8035 | 0.0305550505008764 | 0.2952380952380952 | 0.0864605957548972 |
| 42 | original_type | federated | rare_random_60 | order_2 | 0.2646310580078917 | 0.0094389782771151 | 0.4702165025629679 | 0.0092353598298255 | 0.9981666666666668 | 0.0037226367928335 | 0.1695454545454545 | 0.0353117003706047 |
| 42 | original_type | federated | rare_random_60 | order_3 | 0.5969449418299704 | 0.0236388474747793 | 0.369636575451891 | 0.0265591190158127 | 0.8116666666666668 | 0.0780708763137385 | 0.4795238095238095 | 0.0109224343294214 |
| 43 | merged_scans | centralized | balanced_rare_60 | order_1 | 0.9075926418028762 | 0.0067663534121246 | 0.0912926111734367 | 0.0068437944331278 | 0.7321666666666667 | 0.0209945613180716 | 0.7814197530864198 | 0.0554603665539091 |
| 43 | merged_scans | centralized | balanced_rare_60 | order_2 | 0.902744551388428 | 0.0265591621331803 | 0.0966904119187225 | 0.0266122569450016 | 0.9818333333333332 | 0.0406539901311082 | 0.7792901234567902 | 0.0477759545134043 |
| 43 | merged_scans | centralized | balanced_rare_60 | order_3 | 0.9170152057643082 | 0.017727906145815 | 0.073207195510608 | 0.019207863126272 | 0.787 | 0.0556321693950985 | 0.7688271604938272 | 0.0455597560897748 |
| 43 | merged_scans | centralized | class_balanced_60 | order_1 | 0.8820916695848446 | 0.0158576225875823 | 0.1145560982604611 | 0.0153155753167999 | 0.6573333333333333 | 0.0468396265707141 | 0.7676234567901234 | 0.0561212718726042 |
| 43 | merged_scans | centralized | class_balanced_60 | order_2 | 0.902744551388428 | 0.0265591621331803 | 0.0966904119187225 | 0.0266122569450016 | 0.9818333333333332 | 0.0406539901311082 | 0.7792901234567902 | 0.0477759545134043 |
| 43 | merged_scans | centralized | class_balanced_60 | order_3 | 0.909289860863104 | 0.0190825656561506 | 0.0838765054521926 | 0.0215555209737372 | 0.7575000000000001 | 0.0666817112654133 | 0.7409259259259259 | 0.0094842352825347 |
| 43 | merged_scans | federated | balanced_rare_60 | order_1 | 0.8948865691888562 | 0.0226388626818904 | 0.1016509578785775 | 0.0224657859676249 | 0.7005 | 0.0690948980625314 | 0.8334728395061729 | 0.0230270133833557 |
| 43 | merged_scans | federated | balanced_rare_60 | order_2 | 0.8731283438433455 | 0.0152793630514862 | 0.1262623667809861 | 0.0152826021638491 | 0.9925 | 0.0186131839641677 | 0.7446604938271605 | 0.0116532954054567 |
| 43 | merged_scans | federated | balanced_rare_60 | order_3 | 0.8756895238478378 | 0.0147307416060206 | 0.1151114134434895 | 0.0170020505775106 | 0.6983333333333334 | 0.0595663340163564 | 0.725951975308642 | 0.0348446132992002 |
| 43 | merged_scans | federated | class_balanced_60 | order_1 | 0.8477683873706745 | 0.0409449649546303 | 0.1487580765260547 | 0.0411777880562609 | 0.5533333333333333 | 0.1215207140804286 | 0.8237816514349847 | 0.0570440529182992 |
| 43 | merged_scans | federated | class_balanced_60 | order_2 | 0.8731283438433455 | 0.0152793630514862 | 0.1262623667809861 | 0.0152826021638491 | 0.9925 | 0.0186131839641677 | 0.7446604938271605 | 0.0116532954054567 |
| 43 | merged_scans | federated | class_balanced_60 | order_3 | 0.855878620102604 | 0.0240715663545129 | 0.1390779206846853 | 0.0246435061596867 | 0.6076666666666667 | 0.0660256216634829 | 0.7163271604938272 | 0.0159716713621766 |
| 43 | original_type | centralized | balanced_rare_60 | order_1 | 0.5769463128707344 | 0.0069697288958124 | 0.1783278289944675 | 0.0079508471600003 | 0.7328333333333333 | 0.0209356745565028 | 0.5020238095238095 | 0.0356703874833155 |
| 43 | original_type | centralized | balanced_rare_60 | order_2 | 0.4118889478924659 | 0.028070432002665 | 0.3226015709702401 | 0.0273648456144297 | 0.9988333333333334 | 0.0022291558497487 | 0.4966666666666667 | 0.0322665657813431 |
| 43 | original_type | centralized | balanced_rare_60 | order_3 | 0.6283324693088443 | 0.0168649298719495 | 0.3498343764105162 | 0.0218990897087543 | 0.8733333333333334 | 0.0445346307196246 | 0.5058333333333334 | 0.0330793898333392 |
| 43 | original_type | centralized | class_balanced_60 | order_1 | 0.5561588872156986 | 0.0164693382232488 | 0.1973736372870911 | 0.0170841566993583 | 0.6611666666666667 | 0.0479715064605934 | 0.4951190476190477 | 0.0361457621993022 |
| 43 | original_type | centralized | class_balanced_60 | order_2 | 0.4118889478924659 | 0.028070432002665 | 0.3226015709702401 | 0.0273648456144297 | 0.9988333333333334 | 0.0022291558497487 | 0.4966666666666667 | 0.0322665657813431 |
| 43 | original_type | centralized | class_balanced_60 | order_3 | 0.6340461030971697 | 0.0154115576425853 | 0.349120263218127 | 0.0194450000173365 | 0.8701666666666666 | 0.039200733805175 | 0.4871428571428571 | 0.0072043210907366 |
| 43 | original_type | federated | balanced_rare_60 | order_1 | 0.5656856509152106 | 0.0232194388326057 | 0.1836699661430404 | 0.0240052160954512 | 0.7008333333333334 | 0.0692697803456587 | 0.5471126984126984 | 0.0110042720580389 |
| 43 | original_type | federated | balanced_rare_60 | order_2 | 0.388483899398901 | 0.0090705916012502 | 0.3471957001143194 | 0.0093602773926561 | 0.9985 | 0.0024152294576982 | 0.474047619047619 | 0.0055214371844209 |
| 43 | original_type | federated | balanced_rare_60 | order_3 | 0.6236227531934619 | 0.0355516930597764 | 0.3410670729867543 | 0.0367081656173082 | 0.8071666666666667 | 0.0718668607844557 | 0.4772619047619048 | 0.0254800842596242 |
| 43 | original_type | federated | class_balanced_60 | order_1 | 0.5173350540373411 | 0.0418037443474296 | 0.2320094998502052 | 0.0420722362184624 | 0.5533333333333333 | 0.1215207140804286 | 0.5362940630797773 | 0.0358896443209588 |
| 43 | original_type | federated | class_balanced_60 | order_2 | 0.388483899398901 | 0.0090705916012502 | 0.3471957001143194 | 0.0093602773926561 | 0.9985 | 0.0024152294576982 | 0.474047619047619 | 0.0055214371844209 |
| 43 | original_type | federated | class_balanced_60 | order_3 | 0.5337343430990958 | 0.0245090700394044 | 0.4599444199104157 | 0.0243606733972646 | 0.6316666666666666 | 0.0701057402415438 | 0.4669047619047619 | 0.0128193644465041 |
| 44 | merged_scans | centralized | balanced_rare_60 | order_1 | 0.9086422132193004 | 0.0149728515380042 | 0.0883235339241615 | 0.0153791030164329 | 0.742 | 0.0475693126518855 | 0.8577911664261665 | 0.0102415267204825 |
| 44 | merged_scans | centralized | balanced_rare_60 | order_2 | 0.8573549433934433 | 0.01557610861496 | 0.1418595714865213 | 0.0155744205252918 | 0.9991666666666668 | 0.0018002057495577 | 0.863835978835979 | 0.002960521165681 |
| 44 | merged_scans | centralized | balanced_rare_60 | order_3 | 0.9395669501642256 | 0.0231161096984364 | 0.0513950294057858 | 0.02650353701224 | 0.8656666666666666 | 0.0862246563230303 | 0.8630423280423282 | 0.0107919269726972 |
| 44 | merged_scans | centralized | class_balanced_60 | order_1 | 0.8928791817642374 | 0.0221759545267307 | 0.104141881232748 | 0.0219822028823549 | 0.6910000000000001 | 0.0679832949706156 | 0.8694760702260703 | 0.0310332514687053 |
| 44 | merged_scans | centralized | class_balanced_60 | order_2 | 0.8573549433934433 | 0.01557610861496 | 0.1418595714865213 | 0.0155744205252918 | 0.9991666666666668 | 0.0018002057495577 | 0.863835978835979 | 0.002960521165681 |
| 44 | merged_scans | centralized | class_balanced_60 | order_3 | 0.9213496568436071 | 0.0203294825225558 | 0.0702453204768927 | 0.0236789137410975 | 0.8026666666666668 | 0.0772849465482312 | 0.8532116702741703 | 0.0120253608188302 |
| 44 | merged_scans | federated | balanced_rare_60 | order_1 | 0.8948715770077446 | 0.0378094199917833 | 0.1029093338112135 | 0.0376183388225048 | 0.6971666666666667 | 0.1158624397217303 | 0.8456413840788841 | 0.0144014925492227 |
| 44 | merged_scans | federated | balanced_rare_60 | order_2 | 0.8280301065752111 | 0.010836288712694 | 0.1713835453774385 | 0.0108685800803955 | 0.9996666666666666 | 0.0010540925533894 | 0.8387273027898028 | 0.0115320287541161 |
| 44 | merged_scans | federated | balanced_rare_60 | order_3 | 0.8977564363729014 | 0.0190980376435741 | 0.0929628725477019 | 0.021856906108184 | 0.7678333333333333 | 0.0712630754733889 | 0.7990063732563732 | 0.0416716523608903 |
| 44 | merged_scans | federated | class_balanced_60 | order_1 | 0.821327905613782 | 0.0205729855923035 | 0.1764530052051761 | 0.0208409593753906 | 0.4701666666666666 | 0.0627873640665042 | 0.8174004930254931 | 0.0134914148039982 |
| 44 | merged_scans | federated | class_balanced_60 | order_2 | 0.8280301065752111 | 0.010836288712694 | 0.1713835453774385 | 0.0108685800803955 | 0.9996666666666666 | 0.0010540925533894 | 0.8387273027898028 | 0.0115320287541161 |
| 44 | merged_scans | federated | class_balanced_60 | order_3 | 0.8701165509605302 | 0.0332184687981475 | 0.1239473941661432 | 0.0343341759809511 | 0.6565 | 0.0974946975449573 | 0.7855511363636364 | 0.0137650715150023 |
| 44 | original_type | centralized | balanced_rare_60 | order_1 | 0.5787344078933132 | 0.015170133322479 | 0.1730952510958787 | 0.0162756270944683 | 0.7448333333333333 | 0.0476707457462121 | 0.5546939393939394 | 0.0108109455269527 |
| 44 | original_type | centralized | balanced_rare_60 | order_2 | 0.4181549433934433 | 0.0370249682656111 | 0.317326238153188 | 0.0367026855912599 | 0.9991666666666668 | 0.0018002057495577 | 0.5518722943722943 | 0.0057963164984409 |
| 44 | original_type | centralized | balanced_rare_60 | order_3 | 0.6542880144107703 | 0.0172713614647895 | 0.3243406318259078 | 0.0200323095444195 | 0.9265 | 0.0245634728312359 | 0.5619588744588745 | 0.0086590983561486 |
| 44 | original_type | centralized | class_balanced_60 | order_1 | 0.5664410734079472 | 0.0189883475770227 | 0.1854439014347682 | 0.0187025347895334 | 0.7048333333333334 | 0.0570490908379099 | 0.5613095238095238 | 0.0236431201327999 |
| 44 | original_type | centralized | class_balanced_60 | order_2 | 0.4181549433934433 | 0.0370249682656111 | 0.317326238153188 | 0.0367026855912599 | 0.9991666666666668 | 0.0018002057495577 | 0.5518722943722943 | 0.0057963164984409 |
| 44 | original_type | centralized | class_balanced_60 | order_3 | 0.6396584162233017 | 0.0129415049232455 | 0.3383920687123475 | 0.0177063396393935 | 0.8718333333333333 | 0.056319470132889 | 0.5588975468975469 | 0.0086606208982135 |
| 44 | original_type | federated | balanced_rare_60 | order_1 | 0.5636600067598107 | 0.0382731018463339 | 0.1873204449223246 | 0.037953447263373 | 0.6973333333333334 | 0.1155774551897909 | 0.5471969696969697 | 0.0089575774707853 |
| 44 | original_type | federated | balanced_rare_60 | order_2 | 0.3939412176863222 | 0.0426086491058935 | 0.3415724342663274 | 0.0419626486232589 | 0.9996666666666666 | 0.0010540925533894 | 0.5414199134199135 | 0.0048231587815235 |
| 44 | original_type | federated | balanced_rare_60 | order_3 | 0.6354659613971535 | 0.0287535307040369 | 0.3276422364123387 | 0.030787857173667 | 0.8523333333333334 | 0.0359200071489448 | 0.5352821067821067 | 0.028129268064743 |
| 44 | original_type | federated | class_balanced_60 | order_1 | 0.4909025612611649 | 0.0241949610047154 | 0.2600778904209704 | 0.0246884793745292 | 0.4753333333333334 | 0.073180817833401 | 0.5312121212121212 | 0.0054420002017137 |
| 44 | original_type | federated | class_balanced_60 | order_2 | 0.3939412176863222 | 0.0426086491058935 | 0.3415724342663274 | 0.0419626486232589 | 0.9996666666666666 | 0.0010540925533894 | 0.5414199134199135 | 0.0048231587815235 |
| 44 | original_type | federated | class_balanced_60 | order_3 | 0.6045798436344253 | 0.0348466852135615 | 0.3622063237144702 | 0.0390821848028593 | 0.734 | 0.0768725094949383 | 0.5325223665223665 | 0.0199273313043625 |
| 45 | merged_scans | centralized | balanced_rare_60 | order_1 | 0.9006558657205369 | 0.0088586452370258 | 0.0935889083027724 | 0.0099325443797252 | 0.7150000000000001 | 0.0286205486053139 | 0.8493827160493828 | 0.0059100438750391 |
| 45 | merged_scans | centralized | balanced_rare_60 | order_2 | 0.8948205553711693 | 0.0154414447318553 | 0.1046262860935944 | 0.0154194816173335 | 0.9898333333333332 | 0.0091439111495634 | 0.8723063973063973 | 0.0155486816051846 |
| 45 | merged_scans | centralized | balanced_rare_60 | order_3 | 0.9235049157964706 | 0.0296413114670882 | 0.069770944517437 | 0.0341164224321795 | 0.7995 | 0.104515490020958 | 0.8568969135802469 | 0.0119194488804321 |
| 45 | merged_scans | centralized | class_balanced_60 | order_1 | 0.8869972692559361 | 0.0147702115454435 | 0.1072475047673732 | 0.0131158117015485 | 0.6783333333333333 | 0.0365401858942341 | 0.8548524931858266 | 0.0286795612253784 |
| 45 | merged_scans | centralized | class_balanced_60 | order_2 | 0.8948205553711693 | 0.0154414447318553 | 0.1046262860935944 | 0.0154194816173335 | 0.9898333333333332 | 0.0091439111495634 | 0.8723063973063973 | 0.0155486816051846 |
| 45 | merged_scans | centralized | class_balanced_60 | order_3 | 0.9126046024313984 | 0.0176747273688008 | 0.0817811704834605 | 0.0201182214034618 | 0.758 | 0.0574606682441279 | 0.8564506172839506 | 0.0108180859093994 |
| 45 | merged_scans | federated | balanced_rare_60 | order_1 | 0.8977291467613405 | 0.0095416844747956 | 0.0998209735163541 | 0.0096147194212718 | 0.7091666666666667 | 0.0308545972723597 | 0.8461907070707071 | 0.0152193152439787 |
| 45 | merged_scans | federated | balanced_rare_60 | order_2 | 0.8652916325552237 | 0.0192665123513487 | 0.1341107644650956 | 0.0193191643843215 | 0.9866666666666668 | 0.0231873741718991 | 0.8555026455026455 | 0.0044173343728897 |
| 45 | merged_scans | federated | balanced_rare_60 | order_3 | 0.87575360307355 | 0.0093652665297352 | 0.1210220175383256 | 0.009323203771216 | 0.6606666666666666 | 0.0222111083319435 | 0.8190819753086419 | 0.0237856529741223 |
| 45 | merged_scans | federated | class_balanced_60 | order_1 | 0.8446892437941861 | 0.0470980755879296 | 0.1528608764835087 | 0.0479396511500809 | 0.5479999999999999 | 0.14499212409432 | 0.8126061375661375 | 0.0211639485153232 |
| 45 | merged_scans | federated | class_balanced_60 | order_2 | 0.8652916325552237 | 0.0192665123513487 | 0.1341107644650956 | 0.0193191643843215 | 0.9866666666666668 | 0.0231873741718991 | 0.8555026455026455 | 0.0044173343728897 |
| 45 | merged_scans | federated | class_balanced_60 | order_3 | 0.8670138696502484 | 0.0314327094808634 | 0.128884164945475 | 0.0328883487158418 | 0.6391666666666667 | 0.0869732824024243 | 0.8248604938271604 | 0.0227868197710391 |
| 45 | original_type | centralized | balanced_rare_60 | order_1 | 0.5753184440427569 | 0.0107392580960936 | 0.1771176063809199 | 0.0109273001867131 | 0.7205 | 0.0318469526809352 | 0.5480952380952381 | 0.0067855982539044 |
| 45 | original_type | centralized | balanced_rare_60 | order_2 | 0.4296538887045028 | 0.0321374242789164 | 0.3039262860935944 | 0.0318310713882411 | 0.9965 | 0.0038849186082326 | 0.5577056277056277 | 0.0145591980811713 |
| 45 | original_type | centralized | balanced_rare_60 | order_3 | 0.6335073870284171 | 0.0405764631799782 | 0.3491018066188238 | 0.0456297852448461 | 0.8550000000000001 | 0.0804654668663812 | 0.5621706864564008 | 0.0081096167571409 |
| 45 | original_type | centralized | class_balanced_60 | order_1 | 0.5621090231585992 | 0.0139156485004384 | 0.1903270272650775 | 0.0129881950545311 | 0.6861666666666666 | 0.0371271588722585 | 0.5534260977118121 | 0.0188020459516801 |
| 45 | original_type | centralized | class_balanced_60 | order_2 | 0.4296538887045028 | 0.0321374242789164 | 0.3039262860935944 | 0.0318310713882411 | 0.9965 | 0.0038849186082326 | 0.5577056277056277 | 0.0145591980811713 |
| 45 | original_type | centralized | class_balanced_60 | order_3 | 0.6285118567931983 | 0.021299063318397 | 0.3519850272327718 | 0.0235627023114155 | 0.8521666666666666 | 0.0552214956357297 | 0.5655364873222016 | 0.0087357013247002 |
| 45 | original_type | federated | balanced_rare_60 | order_1 | 0.5685615618210283 | 0.0097373682052428 | 0.1832413591912852 | 0.0106585328201559 | 0.7095 | 0.0301339601704714 | 0.5478402597402597 | 0.0059215605401619 |
| 45 | original_type | federated | balanced_rare_60 | order_2 | 0.3931248220673378 | 0.0112064378697719 | 0.3410331305085371 | 0.0112558204330446 | 0.9976666666666668 | 0.0041722185234485 | 0.5460606060606061 | 0.0062899684037198 |
| 45 | original_type | federated | balanced_rare_60 | order_3 | 0.5503411260113429 | 0.0083404148635729 | 0.443267827933866 | 0.0083626068253417 | 0.6768333333333334 | 0.0116917719300453 | 0.547547619047619 | 0.015305411002194 |
| 45 | original_type | federated | class_balanced_60 | order_1 | 0.5144447993497415 | 0.0477368011611603 | 0.237358121662572 | 0.0484784142922134 | 0.5479999999999999 | 0.14499212409432 | 0.5321868480725623 | 0.0079131899231979 |
| 45 | original_type | federated | class_balanced_60 | order_2 | 0.3931248220673378 | 0.0112064378697719 | 0.3410331305085371 | 0.0112558204330446 | 0.9976666666666668 | 0.0041722185234485 | 0.5460606060606061 | 0.0062899684037198 |
| 45 | original_type | federated | class_balanced_60 | order_3 | 0.5932997835824375 | 0.0235946222036099 | 0.3760426954577303 | 0.0257420821714057 | 0.7286666666666667 | 0.0677221994348699 | 0.5451065141207998 | 0.0104694698134822 |

## split_consistency.csv

| score_space | environment | metric | splits | positive_differences | negative_differences | significant_better | significant_worse |
|---|---|---|---|---|---|---|---|
| merged_scans | centralized | forgetting | 4 | 0 | 4 | 2 | 0 |
| merged_scans | centralized | old_task_accuracy | 4 | 4 | 0 | 3 | 0 |
| merged_scans | centralized | slowloris_recall | 4 | 4 | 0 | 2 | 0 |
| merged_scans | centralized | worst_client_macro_recall | 4 | 2 | 2 | 1 | 0 |
| merged_scans | federated | forgetting | 4 | 0 | 4 | 4 | 0 |
| merged_scans | federated | old_task_accuracy | 4 | 4 | 0 | 4 | 0 |
| merged_scans | federated | slowloris_recall | 4 | 4 | 0 | 4 | 0 |
| merged_scans | federated | worst_client_macro_recall | 4 | 4 | 0 | 1 | 0 |
| original_type | centralized | forgetting | 4 | 0 | 4 | 2 | 0 |
| original_type | centralized | old_task_accuracy | 4 | 4 | 0 | 2 | 0 |
| original_type | centralized | slowloris_recall | 4 | 4 | 0 | 3 | 0 |
| original_type | centralized | worst_client_macro_recall | 4 | 2 | 2 | 1 | 0 |
| original_type | federated | forgetting | 4 | 1 | 3 | 3 | 0 |
| original_type | federated | old_task_accuracy | 4 | 4 | 0 | 3 | 0 |
| original_type | federated | slowloris_recall | 4 | 4 | 0 | 3 | 0 |
| original_type | federated | worst_client_macro_recall | 4 | 4 | 0 | 0 | 0 |

## Calibration choices

```json
{
  "test_data_used": false,
  "selected": [
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      }
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      }
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      }
    }
  ],
  "trials": [
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5735860259718834
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5717009473863593
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5752012739384676
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5768698412245181
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5730897503881913
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5777386409268368
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5923094830188371
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5887913769394839
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5982736044373016
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5953065388377192
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5943310572130172
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7049958282458283
    },
    {
      "split_seed": 43,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5944062861167538
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7129282770557825
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7049958282458283
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7049958282458283
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7129282770557825
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7129282770557825
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7245149815127543
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7313662051880314
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7245149815127543
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7313662051880314
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7245149815127543
    },
    {
      "split_seed": 43,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7313662051880314
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.793064235813679
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7724350574876744
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7949479692130026
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7958325560441373
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7958182983394564
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7893009219601647
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8684496031066187
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8717066177450364
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8814735864440764
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8717998496183351
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8834604328073147
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5692408556345081
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.561752157374095
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5665681673560292
    },
    {
      "split_seed": 43,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8782896211270376
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5666052868808993
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5626127941801662
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5659533864428075
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5673236910948491
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5718979301445893
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5664211534155855
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.573531271726706
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5625142409351763
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6968802401302401
    },
    {
      "split_seed": 44,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5635907896442418
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.6938450098940077
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6968802401302401
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6968802401302401
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.6938450098940077
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.6938450098940077
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.717961307314314
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7170803848465318
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.717961307314314
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7170803848465318
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.717961307314314
    },
    {
      "split_seed": 44,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7170803848465318
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7663986335573195
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7895599282038591
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7583344580232109
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7748150829002722
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7727583931370122
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7719958137424731
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8054914934422174
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7879354945145591
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8115766621298359
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8070323154017475
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.806019343396849
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5519332467211087
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5530442723983926
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5529526059810024
    },
    {
      "split_seed": 44,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8218530788583684
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5522302029200693
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5568272469096522
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5536720872956953
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5633262688396319
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5704476084420406
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5769094512474245
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5682985529277289
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5783579375956882
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6781889415541976
    },
    {
      "split_seed": 45,
      "order": "order_1",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5748395840528358
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.685160541945063
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6781889415541976
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.6781889415541976
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.685160541945063
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.685160541945063
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7033724271274382
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7033724271274382
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7142447708605838
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7142447708605838
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7033724271274382
    },
    {
      "split_seed": 45,
      "order": "order_2",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7142447708605838
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7737168969980774
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7843804029530643
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7847400086612225
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7472161839542129
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7765465707269716
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "federated",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7824412440751528
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8045961324310433
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8198189860024493
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "class_balanced_60",
      "settings": {
        "learning_rate": 0.003,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8236356567935077
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8163309673601991
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8373729584261321
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5260498697870636
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5216164168463723
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5189575246579701
    },
    {
      "split_seed": 45,
      "order": "order_3",
      "environment": "centralized",
      "method": "balanced_rare_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8244338963127938
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5496805688125287
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5226356777553882
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5440266317860972
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5395131597553646
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5935538518645422
    },
    {
      "split_seed": 42,
      "order": "order_1",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5374672976532665
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5861561336049087
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5935538518645422
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5869232276220027
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.5861561336049087
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.5869232276220027
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.569416466792302
    },
    {
      "split_seed": 42,
      "order": "order_2",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.569416466792302
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7614017569908438
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7747168192691578
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.7680632269240287
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "federated",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.7765256537160768
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.25
      },
      "selection_score": 0.8164105966725678
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.25
      },
      "selection_score": 0.784700641342902
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.1,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8188276210508949
    },
    {
      "split_seed": 42,
      "order": "order_3",
      "environment": "centralized",
      "method": "rare_random_60",
      "settings": {
        "learning_rate": 0.003,
        "rare_quota_fraction": 0.2,
        "replay_fraction": 0.5
      },
      "selection_score": 0.8082946671615937
    }
  ]
}
```

## Memory and allocation components

Memory 60 means at most 60 stored fitting flows per client, not epochs or test examples. Five clients can retain 300 flows in total; centralized comparison receives 300 slots. A 10% rare reservation means up to six reserved slots per client when candidates exist, and 20% means up to twelve. The remainder can retain additional rare examples; the reservation is a minimum, not a cap. This round does not change the accepted MLP or sweep additional model hyperparameters.

| Policy | Rare reservation | Remaining slots | Separate benign reservation |
|---|---|---|---|
| Class-balanced | None | Feasible class-balanced | None; ordinary class |
| Protected | Fixed 20% | Uniform random | Fixed 20% when feasible |
| Balanced+rare | Calibration-selected 10%/20%, balanced within rare group | Feasible class-balanced | None; ordinary class |
| Rare+random | Calibration-selected 10%/20%, uniform within rare group | Uniform random | None; ordinary class |

## Ablation interpretation

Rare+random removes the benign reservation and random-fills after a rare minimum. Its quota is calibrated at 10%/20%, while the historical protected quota was fixed at 20%. Thus comparisons show allocation-policy performance and do not isolate a single causal benign-quota effect when selected rare quotas differ. Balanced+rare also balances inside the reserved group, whereas the protected-style rare+random reservation samples uniformly within that group. This is not a fully crossed component factorial. All losses are reported.
