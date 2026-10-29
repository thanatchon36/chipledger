---
title: "Is Huang's Law Moore's Law? Decomposing a Decade of AI Accelerator Performance Growth, 2012–2026"
author: "Thanatchon Chongmankhong"
date: "October 2026"
bibliography: paper/refs.bib
csl: paper/csl/ieee.csl
link-citations: true
numbersections: true
section-numbering: "1.1"
mainfont: "Libertinus Serif"
fontsize: 10pt
papersize: a4
margin:
  x: 2.2cm
  y: 2.4cm
abstract: |
  The peak throughput that vendors publish for their data-centre AI accelerators has grown far faster than the
  transistor counts behind it, a pattern that has been called Huang's law. We ask how much of that growth is
  Moore's law. From vendor documents we build a dataset of {{population.products}} accelerators from
  {{population.vendors}} vendors, announced 2012–2026, with a source, an access date and a confidence level for
  each of its {{population.source_rows|,}} values, and split headline peak throughput exactly into transistor
  density, die area, clock, operations per transistor per cycle at 16-bit precision (specialization) and the gain
  from narrower number formats (precision). The design was pre-registered before any value was collected. Over
  the {{population.A_flagships}} flagships for which every term is published, headline dense throughput doubled
  every {{hypotheses.H1.doubling|.2f}} years (95% CI {{hypotheses.H1.doubling_ci[0]|.2f}}–{{hypotheses.H1.doubling_ci[1]|.2f}})
  and transistor density every {{hypotheses.H2.a_density_doubling|.2f}} years. From NVIDIA's K20X to its H100,
  headline throughput rose {{estimator_c.headline_ratio|x0}}; density accounts for
  {{estimator_a.nvidia_a.cumulative.shares.density_mtr_mm2|pct}} of that gain on a log scale, specialization for
  {{estimator_a.nvidia_a.cumulative.shares.spec_ops_per_transistor_cycle|pct}}, clock for
  {{estimator_a.nvidia_a.cumulative.shares.boost_clock_mhz|pct}}, precision for
  {{estimator_a.nvidia_a.cumulative.shares.precision_multiplier|pct}} and die area for
  {{estimator_a.nvidia_a.cumulative.shares.area_mm2|pct}}. Moore's law in the density sense is therefore about a
  third of Huang's law, a share that sits just under our pre-registered threshold. Our total agrees with NVIDIA's
  own account of the same decade, but the split does not: transistors times clock grew
  {{estimator_c.physical_nf|x1}}, against the {{estimator_c.nvidia.process|x1}} NVIDIA credits to process,
  because NVIDIA counts the extra transistors as architecture. In the cross-vendor regression we cannot tell the
  architectural and arithmetic terms apart from density, so one pre-registered hypothesis is falsified. Memory
  bandwidth doubled every {{rq4_memory.mem_bandwidth_gbs.fit.doubling_years|.2f}} years, and per-accelerator
  MLPerf results grew more slowly than headline peaks on all four NVIDIA benchmarks we could follow. Since H100,
  no vendor in the sample has published both die area and clock for its flagship, so the full decomposition ends
  in 2022.
---

<!-- Independent personal research. Every number below is filled from results/numbers.json by `chipledger paper`. -->

# Introduction

In 1965 Gordon Moore predicted that the number of components on an integrated circuit would keep doubling
every year [@moore1965], and in 1975 he forecast that the rate would slow to a doubling every two years
[@moore1975]. Fifty years later the
fastest-growing number in computing is not a transistor count but the peak throughput printed on the datasheets
of AI accelerators. NVIDIA's chief scientist has described a thousand-fold gain in single-chip inference
throughput over the decade from Kepler to Hopper [@dally2023hotchips], and the pattern has been called "Huang's
law" since 2018 [@perry2018spectrum; @mims2020]. If peak throughput grows much faster than transistor counts, most of the growth must
come from somewhere other than the process node, and it matters where. Process gains have been steady for half a
century, whereas the alternatives (larger dies, higher clocks, more arithmetic per transistor, narrower number
formats) each have a limit that a forecast of AI compute would need to know about.

This paper asks a narrow, checkable version of the question: *how much of the growth in the vendor-published peak
throughput of data-centre AI accelerators is Moore's law?* We answer it with an accounting identity rather than a
model. For every accelerator whose vendor publishes the transistor count, the die area, the clock and the peak
rates, the logarithm of the headline peak rate splits exactly into five terms: transistor density, die area,
clock, specialization (operations per transistor per cycle at a 16-bit reference precision) and a precision
multiplier (the gain from formats narrower than 16-bit). Moore's law in its scaling sense is the density
term.

Our answer is that density supplies about a third of the growth (Figure @fig:f2). From K20X to H100, the
headline rate rose {{estimator_c.headline_ratio|x0}}, or {{estimator_a.nvidia_a.cumulative.dlog2_headline|.2f}}
doublings in {{estimator_a.nvidia_a.cumulative.years|.1f}} years, of which density supplied
{{estimator_a.nvidia_a.cumulative.dlog2.density_mtr_mm2|.2f}} and specialization
{{estimator_a.nvidia_a.cumulative.dlog2.spec_ops_per_transistor_cycle|.2f}}. Across vendors, the flagships'
headline rate doubled every {{hypotheses.H1.doubling|.2f}} years and their density every
{{hypotheses.H2.a_density_doubling|.2f}} years (Figure @fig:f1). The precision multiplier, often named as the main
driver, moved in single steps rather than along a trend. The decade's largest architectural gains came from
matrix units at 16-bit precision. The result agrees in total with NVIDIA's own decomposition of the same decade
and disagrees with it on where the transistors belong (Section @sec:recon).

We make three contributions. The first is a dataset of {{population.products}} accelerators, each value with a
source, an access date and a confidence level, released with the code under open licences. The second is a
pre-registered decomposition, reported whatever the outcome; two of the seven hypotheses fail. The third is a
quantitative reconciliation with the vendor's own account, which shows that the two accountings differ in
bookkeeping rather than in fact.

# Background

**Moore, Dennard and Koomey.** Moore's 1965 paper projected the number of components per chip at minimum cost
[@moore1965]. In 1975 he split the growth of chip complexity into larger dies, finer dimensions and a residual of
"circuit and device cleverness", the first decomposition of this kind, and forecast the two-year cadence usually
quoted [@moore1975]. Dennard and colleagues showed that shrinking
a MOSFET's dimensions and voltage together keeps power density constant [@dennard1974]; when voltage scaling
stalled in the mid-2000s, clock rates stopped rising and the gains from a new node had to be spent on more
cores or more specialised logic [@esmaeilzadeh2011]. Koomey and colleagues measured the efficiency of computing,
peak computations per kilowatt-hour, and found that it doubled every 1.57 years from 1946 to 2009 <!-- numbers-ok: quoted from the cited source -->
[@koomey2011]. Nagy and colleagues hindcast 62 technologies and found that an exponential trend in time forecasts <!-- numbers-ok: quoted from the cited source -->
nearly as well as Wright's law, while warning that short, noisy series fit it only loosely [@nagy2013].

**Specialization as the successor to scaling.** Leiserson and colleagues argued that after Moore's law,
performance must come from "the Top" of the computing stack, software, algorithms and hardware architecture,
and that domain-specific hardware can run applications tens to hundreds of times faster by using fewer
transistors [@leiserson2020]. Thompson and colleagues showed that the computation used by deep learning grew far
faster than per-chip hardware, mostly by running models longer on more machines [@thompson2020limits]. Jouppi and colleagues documented Google's TPUs, the
clearest case of a domain-specific accelerator built for machine learning [@jouppi2017; @jouppi2023]. Khan and
Mann explained for a policy audience why such chips outperform general-purpose processors [@khan2020].

**Huang's law and the vendor's decomposition.** IEEE Spectrum named "Huang's law" in 2018, reporting Jensen
Huang's claim that NVIDIA's GPUs were 25 times faster than five years earlier, where Moore's law would have given <!-- numbers-ok: quoted from the cited source -->
a factor of 10 [@perry2018spectrum]; the Wall Street Journal put <!-- numbers-ok: quoted from the cited source -->
the term in a headline in 2020 [@mims2020]. Dally, Keckler and Kirk reported a 317× gain in GPU inference <!-- numbers-ok: quoted from the cited source -->
performance from Kepler in 2012 to Ampere in 2020, "largely due to the addition of DL-specific data types and
instructions", and expected it to slow toward the 35% a year that technology alone provides <!-- numbers-ok: quoted from the cited source -->
[@dally2021micro]. Dally's Hot Chips 2023 keynote extended the
chart to H100 and split its thousand-fold gain into number representation, complex instructions, process and
sparsity [@dally2023hotchips; @merritt2023nvblog]. That decomposition is the vendor account we test in Section
@sec:recon.

**Trend studies.** Sun and colleagues fitted design trends for more than four thousand CPUs and GPUs from product
data and found clock frequency to be the main driver of GPU FLOPS growth, measured at FP32 and base clock
[@sun2019]. Epoch AI estimated that the FP32 price-performance of GPUs doubles about every 2.5 years <!-- numbers-ok: quoted from the cited source -->
[@hobbhahn2022gpu], and that the FP32 peak of machine learning hardware doubles every 2.3 years and its memory <!-- numbers-ok: quoted from the cited source -->
bandwidth every 4 years, with tensor formats giving a further, roughly constant multiple at each precision <!-- numbers-ok: quoted from the cited source -->
[@epoch2023hardware; @rahman2024epochinsight]. Epoch also
maintains the hardware database we use as a cross-check [@epoch2026database]. Sevilla and colleagues measured the growth of training compute [@sevilla2022], and Ho and
colleagues the algorithmic progress that adds to it [@ho2024]; both are demand-side counterparts of the supply
side studied here. None of these studies splits a chip's peak rate into an exact sum of physical and
architectural terms with a source for every input, and none reconciles a vendor's own account.

**Memory wall and realized performance.** Gholami and colleagues showed that the peak compute of server hardware
has outgrown memory and interconnect bandwidth for two decades, at 3.0× every two years against 1.6× for DRAM <!-- numbers-ok: quoted from the cited source -->
bandwidth and 1.4× for interconnect bandwidth [@gholami2024]. Jouppi and colleagues reported that four of the six <!-- numbers-ok: quoted from the cited source -->
production workloads on the first TPU were memory-bound [@jouppi2017], and split one TPU generation's peak gain
into more matrix units and a higher clock while memory bandwidth rose much less [@jouppi2023]. MLPerf provides measured training and inference throughput on fixed tasks [@mattson2020;
@reddi2020], which we use to check whether realized performance follows the headline peaks.

# Data {#sec:data}

**Unit and population.** The unit is a product: a distinct silicon configuration sold or deployed as a data-centre
machine learning accelerator, announced between 2012 and 2026. Variants of the same silicon that differ in
memory, power or form factor are separate rows linked to a primary variant, the highest-TDP module form; only
primary variants enter the analyses. The dataset has {{population.products}} products from
{{population.vendors}} vendors, {{population.primary}} of them primary. Within each vendor and architecture
generation, the *flagship* is the primary part with the highest headline dense rate among parts positioned for
training; there are {{population.flagships}}. One card whose rates are given for an unstated number of chips is
excluded from every analysis.

**Fields.** For each product we record the announce and ship dates, process node and foundry, transistor count,
compute and total die area, number of compute dies, boost clock, TDP, memory capacity and bandwidth, and every
published peak rate: vector FP64, FP32, FP16, BF16 and INT8, and matrix-unit rates from FP64 down to FP4 and
INT4, dense and, separately, with structured sparsity. Prices are recorded where a vendor publishes them; none
does for the products in the sample, so no per-dollar analysis is possible.

**Sources.** Every value carries a URL, an access date and a confidence level in `data/sources.csv`. The order of
preference is the vendor's datasheet, whitepaper or product page, then a vendor-authored paper, then Epoch AI's
hardware database [@epoch2026database] at medium confidence where the vendor is silent. Of the
{{population.source_rows|,}} source rows, {{population.source_confidence.high|,}} are high confidence,
{{population.source_confidence.medium}} medium and {{population.source_confidence.low}} low. Where sources
disagree, the vendor's document wins and the alternatives are listed in `data/conflicts.md`. Where a vendor
publishes only a sparse rate and states that dense is half of it, the dense rate is derived and marked as such.
A validator rejects any value without a source.

**Coverage.** The decomposition needs five fields (transistor count, compute die area, clock, TDP and a reference
rate), and publication of these has declined. NVIDIA has not published die area or boost clock for Blackwell or
Rubin, AMD has not published die area since MI100, and Google publishes neither transistor count nor die area for
its TPUs. Only {{population.A_flagships}} flagships have all five fields; {{population.A_prime_flagships}} have
every field except die area and {{population.clock_free_flagships}} every field except the clock. We use the
last two groups with reduced identities (Section @sec:method). `data/coverage.md` lists, for every product, the
fields it lacks.

# Method {#sec:method}

**Definitions.** The headline dense rate $P$ is the largest dense peak rate over every supported format, INT8 and
INT4 included, counting two operations per multiply–accumulate. The reference rate $R$ is the dense matrix-unit
FP16 or BF16 rate; if the product has no matrix unit, its vector FP16 or BF16 rate; if it has no 16-bit format, its
FP32 rate. $N$ is the transistor count of the package, $A$ the total area of its compute dies, $f$ the boost
clock (the clock at which vendors state their peak rates, unlike the base clock used by Sun and colleagues
[@sun2019]) and $W$ the TDP.

**Identity A.** For every product with all five fields, by construction,
$$\log_2 P = \log_2 \frac{N}{A} + \log_2 A + \log_2 f + \log_2 \frac{R}{N f} + \log_2 \frac{P}{R},$$
that is, density + area + clock + specialization + precision. Specialization is reference operations per
transistor per cycle: it rises when more of the silicon does 16-bit arithmetic every cycle, and falls when
transistors go to caches, I/O or features that do not raise $R$. Sparsity is outside $P$. Two reduced identities
cover products with missing fields: identity A′ merges density and area into $N$, for products without a
published die area, and the clock-free identity merges the clock into specialization ($R / N$), for products
without a published clock. Identity B splits $P$ into $P/W$ and $W$, and identity C into $P/A$ and $A$.

**Estimators.** Estimator (a) chains NVIDIA's first flagship of each architecture from K20X (Kepler) onward
and reports, for each step and cumulatively, the change in each term's $\log_2$ and its share of the change in
$\log_2 P$. Estimator (b) regresses $\log_2$ of each term and of $P$ on decimal announce year over the flagships
with all five fields; because the identity is additive, the slopes add up to the slope of $P$. Doubling time is
the inverse slope. Intervals are percentile intervals from a bootstrap over chips (2,000 draws), with HC3 <!-- numbers-ok: design constant -->
standard errors and the Theil–Sen slope as checks. Estimator (c) computes identity A from K20X to H100 at the
endpoint rates NVIDIA uses (FP32 for K20X, dense FP8 for H100) and compares its physical part, $N f$, with
NVIDIA's "process" factor, and its architectural part, specialization × precision, with NVIDIA's number
representation × complex instructions [@dally2023hotchips].

**Pre-registration.** The question, the definitions, the sample rule, the estimators, seven hypotheses with
their decision rules and the sensitivity analyses were frozen at the git tag `prereg-v1` before any value was
collected. The thresholds were set after the author had worked the identity through from remembered headline
figures, so the pre-registration is not blind. Every later change, including four decisions taken at review
gates during data collection, is logged with its date and reason in `DEVIATIONS.md`; the main ones are
described where they matter below.

# Results

## How fast {#sec:rate}

Figure @fig:f1 shows the ladder. Over all {{rq1_throughput.flagships.headline.n}} flagships with a headline
rate, the headline doubled every {{rq1_throughput.flagships.headline.fit.doubling_years|.2f}} years (95% CI
{{rq1_throughput.flagships.headline.fit.doubling_ci[0]|.2f}}–{{rq1_throughput.flagships.headline.fit.doubling_ci[1]|.2f}}),
the 16-bit reference rate every {{rq1_throughput.flagships.ref_tflops.fit.doubling_years|.2f}} years and the
vector FP32 rate every {{rq1_throughput.flagships_ladder.fp32.fit.doubling_years|.2f}} years, slower than Epoch
AI's 2.3 years for the FP32 peak of machine learning hardware in general [@epoch2023hardware]. <!-- numbers-ok: quoted from the cited source --> Transistors per
package doubled every {{rq1_throughput.flagships.transistors_b.fit.doubling_years|.2f}} years, close to Moore's
1975 cadence, and transistor density every {{rq1_throughput.flagships_density.density_mtr_mm2.fit.doubling_years|.2f}}
years. On the {{hypotheses.H1.n}} flagships with all five fields, the headline doubled every
{{hypotheses.H1.doubling|.2f}} years (CI {{hypotheses.H1.doubling_ci[0]|.2f}}–{{hypotheses.H1.doubling_ci[1]|.2f}}),
which meets H1. The headline rate has therefore doubled two to three times as fast as density, and the rest of
this section asks where the difference comes from.

![Flagships against announce year, log scale, with least-squares trends and 95% bootstrap intervals for the
doubling time. (a) Peak rates: headline dense (largest dense rate over all formats), 16-bit reference and vector
FP32. (b) Transistors per package, transistor density and compute die area. Hollow markers: wafer-scale parts,
which are included in every fit. Each series is fitted on the flagships that publish
it.](results/figures/f1_ladder.svg){#fig:f1 width=100%}

## Where it comes from {#sec:decomp}

**The NVIDIA chain.** Figure @fig:f2 gives the chain decomposition. From K20X to H100, density contributed
{{estimator_a.nvidia_a.cumulative.shares.density_mtr_mm2|.3f}} of the change in $\log_2 P$, die area
{{estimator_a.nvidia_a.cumulative.shares.area_mm2|.3f}}, clock {{estimator_a.nvidia_a.cumulative.shares.boost_clock_mhz|.3f}},
specialization {{estimator_a.nvidia_a.cumulative.shares.spec_ops_per_transistor_cycle|.3f}} and precision
{{estimator_a.nvidia_a.cumulative.shares.precision_multiplier|.3f}}. The steps differ in kind. The
Kepler-to-Maxwell step came mostly from clock, on the same 28 nm node. <!-- numbers-ok: node name --> Pascal to Volta
added tensor cores and raised specialization by {{estimator_a.nvidia_a.steps[2].dlog2_spec_ops_per_transistor_cycle|.2f}}
doublings in one step. Volta to Ampere took the headline to INT4, a precision gain of
{{estimator_a.nvidia_a.steps[3].dlog2_precision_multiplier|.2f}} doublings, and Hopper's headline format, FP8, is
one step wider than Ampere's INT4, so the precision term fell by
{{estimator_a.nvidia_a.steps[4].dlog2_precision_multiplier|.2f}} doublings in the last step. Die area barely moved
because K20X was already a large die. AMD's Instinct chain from MI60 to MI355X, with identity A′ because AMD
does not publish die area, gives transistors {{estimator_a.amd_a_prime.cumulative.shares.transistors_mtr|.3f}},
clock {{estimator_a.amd_a_prime.cumulative.shares.boost_clock_mhz|.3f}}, specialization
{{estimator_a.amd_a_prime.cumulative.shares.spec_ops_per_transistor_cycle|.3f}} and precision
{{estimator_a.amd_a_prime.cumulative.shares.precision_multiplier|.3f}} of its
{{estimator_a.amd_a_prime.cumulative.dlog2_headline|.2f}} doublings.

![Chain-linked decomposition (estimator a). (a) Change in each term's $\log_2$ for each step of the NVIDIA chain,
identity A; dots: change in the headline rate, the sum of the bars. The steps from H100 onward cannot be
decomposed because NVIDIA does not publish die area or boost clock for Blackwell or Rubin. (b) Each term's share of
the cumulative change in $\log_2 P$: NVIDIA K20X → H100 (identity A) and AMD MI60 → MI355X (identity A′, where
transistors stand for density × area).](results/figures/f2_chain.svg){#fig:f2 width=100%}

**H2: Moore's law proper is the minority.** Density's share of the NVIDIA chain,
{{hypotheses.H2.b_density_share|.3f}}, is below one third, and its doubling time across flagships,
{{hypotheses.H2.a_density_doubling|.2f}} years, is above 2.5 years, so H2 is supported. <!-- numbers-ok: pre-registered thresholds --> The
margin is thin: a change of {{hypotheses.H2.b_margin_endpoint_change|pct1}} in the transistor count or die
area of either endpoint would move the share to one third.

**H3: architecture and arithmetic outweigh density.** In the chain, specialization and precision together
account for {{hypotheses.H3.a_arch_share|.3f}} of the gain against density's {{hypotheses.H3.a_density_share|.3f}},
so part (a) holds. In the regression (Table @tbl:trend, Figure @fig:f3), the specialization and precision slopes
sum to more than the density slope by {{hypotheses.H3.b_contrast.estimate|.3f}} doublings per year, but its
95% interval runs from {{hypotheses.H3.b_contrast.ci[0]|.3f}} to {{hypotheses.H3.b_contrast.ci[1]|.3f}}. Part (b)
fails and H3 is falsified as pre-registered. With nine products, the regression cannot separate the
architectural terms from density, even though the chain puts them ahead.

: Estimator (b): trends of identity A's terms over the {{estimator_b.n}} flagships with all five fields
(K40, M40, P100, V100, MI60, A100, GC200, WSE-2, H100). Slopes in doublings per year with 95% bootstrap intervals;
the term slopes add up to the headline slope. {#tbl:trend}

| term | slope (doublings/yr) | 95% CI | doubling time (yr) |
|---|---|---|---|
| headline rate $P$ | {{estimator_b.fits.headline.slope\|.3f}} | [{{estimator_b.fits.headline.slope_ci[0]\|.3f}}, {{estimator_b.fits.headline.slope_ci[1]\|.3f}}] | {{estimator_b.fits.headline.doubling_years\|.2f}} |
| density $N/A$ | {{estimator_b.fits.density_mtr_mm2.slope\|.3f}} | [{{estimator_b.fits.density_mtr_mm2.slope_ci[0]\|.3f}}, {{estimator_b.fits.density_mtr_mm2.slope_ci[1]\|.3f}}] | {{estimator_b.fits.density_mtr_mm2.doubling_years\|.2f}} |
| area $A$ | {{estimator_b.fits.area_mm2.slope\|.3f}} | [{{estimator_b.fits.area_mm2.slope_ci[0]\|.3f}}, {{estimator_b.fits.area_mm2.slope_ci[1]\|.3f}}] | {{estimator_b.fits.area_mm2.doubling_years\|.2f}} |
| clock $f$ | {{estimator_b.fits.boost_clock_mhz.slope\|.3f}} | [{{estimator_b.fits.boost_clock_mhz.slope_ci[0]\|.3f}}, {{estimator_b.fits.boost_clock_mhz.slope_ci[1]\|.3f}}] | {{estimator_b.fits.boost_clock_mhz.doubling_years\|.2f}} |
| specialization $R/(Nf)$ | {{estimator_b.fits.spec_ops_per_transistor_cycle.slope\|.3f}} | [{{estimator_b.fits.spec_ops_per_transistor_cycle.slope_ci[0]\|.3f}}, {{estimator_b.fits.spec_ops_per_transistor_cycle.slope_ci[1]\|.3f}}] | {{estimator_b.fits.spec_ops_per_transistor_cycle.doubling_years\|.2f}} |
| precision $P/R$ | {{estimator_b.fits.precision_multiplier.slope\|.3f}} | [{{estimator_b.fits.precision_multiplier.slope_ci[0]\|.3f}}, {{estimator_b.fits.precision_multiplier.slope_ci[1]\|.3f}}] | {{estimator_b.fits.precision_multiplier.doubling_years\|.2f}} |

![Regression decomposition (estimator b). (a) Trend of each term, in doublings per year, with 95% bootstrap
intervals, for identity A and the two reduced identities on the flagships each covers. (b) The H3b contrast,
specialization + precision − density, under each sensitivity analysis; orange intervals exclude
zero.](results/figures/f3_regression.svg){#fig:f3 width=100%}

**H4: bigger silicon and more watts.** After 2020 the chain has a single step that can be decomposed, A100 to
H100. On it, TDP grew by {{hypotheses.H4.mean_dlog2_tdp_w_late|.2f}} doublings against a mean of
{{hypotheses.H4.mean_dlog2_tdp_w_early|.2f}} on earlier steps, but die area shrank by
{{hypotheses.H4.mean_dlog2_area_mm2_late|.2f}} doublings against an earlier mean of
{{hypotheses.H4.mean_dlog2_area_mm2_early|.2f}}, so H4 is not supported. Area growth after H100 has come from
putting two dies in a package, which NVIDIA has not quantified. TDP alone, over the full chain to B300, grew by
{{hypotheses.H4.supplementary_tdp_full_chain.mean_dlog2_tdp_w_late|.2f}} doublings per step after 2020 against
{{hypotheses.H4.supplementary_tdp_full_chain.mean_dlog2_tdp_w_early|.2f}} before. In identity B over the same
chain, the power budget accounts for {{estimator_a.nvidia_b.cumulative.shares.tdp_w|.3f}} of the gain and
efficiency for {{estimator_a.nvidia_b.cumulative.shares.tflops_per_w|.3f}}.

## The vendor's account {#sec:recon}

Dally's chart of "single-chip inference performance" plots peak INT8-equivalent TOPS from K20X to H100, and his
slide attributes the gain to number representation ({{estimator_c.nvidia.number_representation|x1}}), complex
instructions ({{estimator_c.nvidia.complex_instructions|x1}}), process ({{estimator_c.nvidia.process|x1}}) and
sparsity ({{estimator_c.nvidia.sparsity|x1}}), which multiply to {{estimator_c.nvidia.total|x0}}, or
{{estimator_c.nvidia.total_dense|x0}} without sparsity [@dally2023hotchips]. The H100 point on the chart, like the
A100 point [@dally2021micro], is a sparse rate, and the slide adds that model efficiency raised the overall gain
further; we compare dense rates and hardware only. Identity A, from K20X's FP32 rate of {{estimator_c.start_rate.tflops|.2f}} TFLOP/s to H100's
dense FP8 rate of {{estimator_c.end_rate.tflops|,.0f}} TFLOP/s, gives {{estimator_c.headline_ratio|x0}}: the
totals agree (Figure @fig:f7, Table @tbl:recon). The split does not. Transistors grew
{{estimator_c.transistor_ratio|x1}} and the clock {{estimator_c.clock_ratio|x2}}, so the physical factor $Nf$ grew
{{estimator_c.physical_nf|x1}}, {{estimator_c.physical_over_nvidia_process|.1f}} times NVIDIA's process factor.
This meets H7. Correspondingly, specialization × precision is {{estimator_c.architecture_spec_x_precision|x1}},
against NVIDIA's {{estimator_c.nvidia.non_physical|x0}}.

The two accountings differ in bookkeeping. NVIDIA's "process" is the gain per transistor from a newer node;
the extra transistors that the node and a larger die make available are credited to the architecture that uses
them. Identity A counts every transistor as a physical input and credits architecture only with what it does
per transistor per cycle. Neither is wrong, but they answer different questions: NVIDIA's says what the design
team did with the transistors it was given; ours says how much of the gain would have arrived without any change
in what a transistor does. Taking FP32 as the reference for every chip, which is closer to NVIDIA's "number
representation", moves most of the architectural gain from specialization to precision
({{estimator_c_fp32_reference.factors.precision_multiplier|x1}} precision and
{{estimator_c_fp32_reference.factors.spec_ops_per_transistor_cycle|x2}} specialization) but leaves the physical
factor where it was.

![NVIDIA's account of K20X → H100 against identity A, as segments of $\log_2$ of the gain. Top: Dally's four
factors [@dally2023hotchips]; sparsity (hatched) is outside the dense comparison. Middle: identity A with the
16-bit reference. Bottom: identity A with FP32 as every chip's reference, where specialization falls below one
and is drawn left of zero. The dashed line marks the dense total. The physical factors (density, area, clock)
multiply to {{estimator_c.physical_nf|x1}}, against {{estimator_c.nvidia.process|x1}} for
process.](results/figures/f7_dally.svg){#fig:f7 width=100%}

: Estimator (c): identity A from K20X to H100 SXM against NVIDIA's account. The FP32-reference column applies
the FP32 sensitivity of Section @sec:robust. {#tbl:recon}

<!-- include: results/tables/t4_reconciliation.md -->

## Efficiency and memory {#sec:mem}

Figure @fig:f4 shows three efficiency ratios. Headline throughput per watt of TDP doubled every
{{rq3_efficiency.tflops_per_w.fit.doubling_years|.2f}} years over {{rq3_efficiency.tflops_per_w.n}} flagships,
the 16-bit reference rate per watt every {{rq3_efficiency.ref_tflops_per_w.fit.doubling_years|.2f}} years,
throughput per mm² of compute die every {{rq3_efficiency.tflops_per_mm2.fit.doubling_years|.2f}} years and per
billion transistors every {{rq3_efficiency.tflops_per_btransistor.fit.doubling_years|.2f}} years. Koomey's
efficiency trend for general computing was a doubling every 1.57 years [@koomey2011]; <!-- numbers-ok: quoted from the cited source --> peak AI throughput per
watt has kept a similar pace, mostly through formats and matrix units rather than voltage.

![Efficiency of flagships: headline rate (a) per watt of TDP, (b) per mm² of compute die and (c) per billion
transistors, log scale, with least-squares trends and 95% bootstrap intervals. No vendor publishes prices for these
products, so no per-dollar series is shown.](results/figures/f4_efficiency.svg){#fig:f4 width=100%}

Memory has not kept up (Figure @fig:f5). Over {{rq4_memory.mem_bandwidth_gbs.n}} flagships, bandwidth doubled
every {{rq4_memory.mem_bandwidth_gbs.fit.doubling_years|.2f}} years and capacity every
{{rq4_memory.mem_capacity_gb.fit.doubling_years|.2f}} years, while the headline rate doubled every
{{rq4_memory.headline.fit.doubling_years|.2f}} years, so the operations available per byte fetched doubled every
{{rq4_memory.ops_per_byte.fit.doubling_years|.2f}} years (fitted directly to the ratio on the flagships that
report bandwidth, so it is not exactly the difference of the two slopes). Flagship bandwidth grew faster than the four-year
doubling Epoch AI found for machine learning hardware in general [@epoch2023hardware], <!-- numbers-ok: quoted from the cited source -->
but not as fast as compute. In the pre-registered test on the decomposition sample
(n = {{hypotheses.H5.n}}), the headline slope exceeds the bandwidth slope by {{hypotheses.H5.contrast.estimate|.3f}}
doublings per year (CI {{hypotheses.H5.contrast.ci[0]|.3f}}–{{hypotheses.H5.contrast.ci[1]|.3f}}), so H5 is
supported; on all {{hypotheses.H5.all_flagships.n}} flagships with both, the gap is
{{hypotheses.H5.all_flagships.contrast.estimate|.3f}} ({{hypotheses.H5.all_flagships.contrast.ci[0]|.3f}}–{{hypotheses.H5.all_flagships.contrast.ci[1]|.3f}}).

![Memory wall. (a) Headline dense rate against memory bandwidth for flagships, coloured by announce year; dashed
lines: constant operations per byte. (b) Headline operations per byte of bandwidth against announce year, with
the least-squares trend; the doubling times of the ratio and of its two parts are given with 95% bootstrap
intervals.](results/figures/f5_memory.svg){#fig:f5 width=100%}

## Peak against measured {#sec:mlperf}

H6 compares the headline trend with MLPerf results, per accelerator, from the first round in which each product
appears. Four benchmarks have results for three NVIDIA flagship generations; no other vendor has three. On all
four, the measured per-accelerator throughput grew more slowly than the headline rate of the same products
(Figure @fig:f6): ResNet-50 training {{hypotheses.H6.benchmarks[benchmark=resnet].slope_realized|.2f}} against
{{hypotheses.H6.benchmarks[benchmark=resnet].slope_headline|.2f}} doublings per year, BERT training
{{hypotheses.H6.benchmarks[benchmark=bert].slope_realized|.2f}} against
{{hypotheses.H6.benchmarks[benchmark=bert].slope_headline|.2f}}, Llama 2 70B LoRA fine-tuning
{{hypotheses.H6.benchmarks[benchmark=llama2_70b_lora].slope_realized|.2f}} against
{{hypotheses.H6.benchmarks[benchmark=llama2_70b_lora].slope_headline|.2f}}, and Llama 2 70B offline inference
{{hypotheses.H6.benchmarks[suite=inference].slope_realized|.2f}} against
{{hypotheses.H6.benchmarks[suite=inference].slope_headline|.2f}}. H6 was pre-registered as exploratory. With three
products per benchmark, results from systems of different sizes and software of different ages, and the BERT
results of the first round excluded because that round's accuracy target was lower, it is a consistency check and
not an estimate of the gap. Software moves these results too: between the first two training rounds, the best
16-chip results improved 1.3× on unchanged hardware [@mattson2020], so a first-round result understates what <!-- numbers-ok: quoted from the cited source -->
the same chip delivers later; Google measured larger compiler-only gains over 20 months on both GPUs and TPUs <!-- numbers-ok: quoted from the cited source -->
[@jouppi2021].

![Peak against measured, NVIDIA flagships. Doublings since the first product of each benchmark, by announce
year, for the headline dense rate and for per-accelerator MLPerf throughput (the first result for each product;
training: inverse time to train per accelerator). (a) BERT training, (b) Llama 2 70B LoRA fine-tuning, (c)
ResNet-50 training, (d) Llama 2 70B inference, offline scenario.](results/figures/f6_mlperf.svg){#fig:f6 width=100%}

## Hypotheses

Table @tbl:hyp collects the seven decisions.

: Pre-registered hypotheses, decision rules and outcomes. CIs are 95% bootstrap intervals. {#tbl:hyp}

<!-- include: results/tables/t1_hypotheses.md -->

# Robustness {#sec:robust}

The pre-registered sensitivity analyses are tabulated in the repository (`results/tables/t5_sensitivity.md`), and
Figure @fig:f3 (b) shows the H3b contrast under each of them. H1 holds in every variant that can be computed:
the headline doubling time ranges from {{sensitivity[label=headline with sparsity].headline_doubling|.2f}} years
with sparsity to {{sensitivity[label=identity A′ (no area)].headline_doubling|.2f}} years with identity A′, and
is {{sensitivity[label=without NVIDIA].headline_doubling|.2f}} years without NVIDIA, on only
{{sensitivity[label=without NVIDIA].n}} products. Density's doubling time stays between
{{sensitivity[label=without wafer-scale].density_doubling|.2f}} and {{sensitivity[label=frontier envelope].density_doubling|.2f}}
years, apart from the same three-product sample ({{sensitivity[label=without NVIDIA].density_doubling|.2f}}).
The H3b contrast is positive in all but one variant, but its interval excludes zero only with FP32 as the
reference, with sparsity in the headline, and with vendor fixed effects over all products in the sample; each of
these changes either the definition or the sample, and none was the primary analysis.

The ship-date variant cannot be computed, because only two of the nine products in the decomposition sample have a
published ship date. On the {{rq1_throughput.flagships_ship_date.headline.n}} flagships that do, the
headline doubling time is {{rq1_throughput.flagships_ship_date.headline.fit.doubling_years|.2f}} years by ship date and
{{rq1_throughput.flagships_ship_date_products_by_announce.headline.fit.doubling_years|.2f}} years by announce date.
The frontier envelope, the products that set a new record when announced, doubles every
{{rq1_throughput.frontier.headline.fit.doubling_years|.2f}} years, and all {{rq1_throughput.all_primary.headline.n}}
primary products every {{rq1_throughput.all_primary.headline.fit.doubling_years|.2f}} years.

**Process nodes.** We also recorded when each product's node entered volume production. Over
{{nodes.n}} products whose node maps onto that series, the median accelerator was announced
{{nodes.median_lag|.1f}} years after its node's volume production began; NVIDIA's median is
{{nodes.median_lag_by_vendor.NVIDIA|.1f}} years. The lag shows no clear trend
({{nodes.trend.slope_years_per_year|.2f}} years per year, CI {{nodes.trend.ci[0]|.2f}}–{{nodes.trend.ci[1]|.2f}}).
Density therefore reaches accelerators with a delay, but the delay has not grown.

# Discussion

**What is left.** The terms of identity A have different futures. Density is the slow, steady term. The clock
has nearly stopped: its trend across flagships is {{estimator_b.fits.boost_clock_mhz.slope|.2f}} doublings per
year. Precision moves in single steps, and they run out: 8-bit floating-point formats for deep learning
[@micikevicius2022] reached the headline with Hopper, and four-bit formats with Blackwell. Each halving of the operand width at most doubles the
peak rate, and the headline formats of current flagships are four bits wide, so at most one or two such steps
remain before arithmetic reaches two bits or one. The area of a single die is bounded by the lithographic reticle,
which H100 already approaches; growth since then has come from packages with more than one die, which raises
the transistor count and, by identity B, power. Specialization has been the largest term after density, and
it is the one with no obvious bound, though its decade was dominated by a single invention, the matrix unit at
16-bit precision.

**What this means for forecasts.** A forecast that extrapolates the headline doubling time of about a year
assumes that the non-density terms keep contributing as they did. Two of them, precision and clock, cannot
contribute at that rate for long, and a third, single-die area, is near its limit. If density keeps doubling
every two to three years and specialization keeps its pace, the headline rate would double more slowly than
in 2012–2022, unless packaging and power budgets keep growing. This is an argument about the composition of the
trend, not a forecast; our data do not identify a break. They also show that the headline rate overstates the
growth of measured throughput (Section @sec:mlperf), and that the memory system falls further behind every
year (Section @sec:mem).

**Disclosure.** The most practical finding may be the coverage problem. In 2012–2020 NVIDIA published transistor
count, die area and clock for every flagship. For Blackwell and Rubin it publishes transistor counts but neither
die area nor boost clock, and other vendors publish less. An exact accounting of where AI hardware gains come
from will soon be impossible from public documents unless vendors publish these five fields again.

# Limitations

The rates are vendor-published peaks, not measured throughput; Section @sec:mlperf shows that the two diverge.
Large training runs report a model FLOPs utilization of about 21–46% of the same peaks [@chowdhery2023], so a <!-- numbers-ok: quoted from the cited source -->
doubling of peak need not double delivered work.
Vendors define peak rates in slightly different ways (boost or sustained clock, with or without the sparsity
factor), and we took them as published, recording derived values as such. The decomposition sample is small,
{{population.A_flagships}} flagships, and NVIDIA-heavy; the intervals reflect sampling over chips, not the
measurement error in vendor figures. TPU and most post-2022 products enter only the throughput trends. No vendor
publishes prices, so we could not compare performance per dollar with Epoch AI's estimates [@hobbhahn2022gpu].
The pre-registration was not blind: the author knew the headline figures of NVIDIA's flagships when setting the
thresholds. Two decision rules were close (H2b and the ship-date variant), and the H3 result is a failure to
detect rather than evidence of absence. The MLPerf comparison uses three products per benchmark and one vendor.

# Conclusion

From 2012 to 2022, the vendor-published peak throughput of AI accelerators doubled about every year, and
transistor density, Moore's law in its scaling sense, supplied about a third of that growth. The rest came mostly
from specialization at 16-bit precision, then from clock and narrower formats, with die area contributing
little. NVIDIA's own account of the same decade agrees in total; it differs in counting the extra transistors as
architecture. Huang's law is therefore not Moore's law, but neither is it independent of it: without density,
the decade's gain would have been about a third smaller on a log scale. Whether the next decade looks the same
depends on terms that the vendors have stopped publishing.

# Data and code availability {-}

The dataset (`data/accelerators.csv`, `data/sources.csv`), the pre-registration, the deviations log and the code
that produces every number, table and figure in this paper are released under CC BY 4.0 (data) and MIT (code)
at `https://github.com/thanatchon36/chipledger`. `make all` rebuilds the analysis from the committed dataset
without network access.

# References {-}

::: {#refs}
:::
