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
term. An identity has two advantages over a regression on chip features. It is exact for every product, so the
shares it reports are bookkeeping facts about the published numbers, with no residual and no model to believe;
and its terms correspond to the mechanisms that forecasts argue about: the process node (density), the size of
the silicon (area), Dennard scaling and its end (clock), what the architecture does with each transistor
(specialization) and the number formats the arithmetic runs at (precision). Its cost is that it needs five
published inputs per product, and, as we show, vendors have stopped publishing two of them.

Our answer is that density supplies about a third of the growth (Figure @fig:f2). From K20X to H100, the
headline rate rose {{estimator_c.headline_ratio|x0}}, or {{estimator_a.nvidia_a.cumulative.dlog2_headline|.2f}}
doublings in {{estimator_a.nvidia_a.cumulative.years|.1f}} years, of which density supplied
{{estimator_a.nvidia_a.cumulative.dlog2.density_mtr_mm2|.2f}} and specialization
{{estimator_a.nvidia_a.cumulative.dlog2.spec_ops_per_transistor_cycle|.2f}}. Across vendors, the flagships'
headline rate doubled every {{hypotheses.H1.doubling|.2f}} years and their density every
{{hypotheses.H2.a_density_doubling|.2f}} years (Figure @fig:f1). The precision multiplier, often named as the main
driver, moved in single steps rather than along a trend. The decade's largest architectural gains came from
matrix units at 16-bit precision. The result agrees in total with NVIDIA's own decomposition of the same decade
and disagrees with it on where the transistors belong (Section @sec:recon). One pre-registered hypothesis fails:
with nine fully documented products, a cross-vendor regression cannot show that the architectural terms outgrow
density, even though the chain within one vendor puts them ahead.

We make three contributions. The first is a dataset of {{population.products}} accelerators, each value with a
source, an access date and a confidence level, released with the code under open licences. The second is a
pre-registered decomposition, reported whatever the outcome; two of the seven hypotheses fail. The third is a
quantitative reconciliation with the vendor's own account, which shows that the two accountings differ in
bookkeeping rather than in fact.

The paper is organised as follows. Section @sec:background places the question among the trend studies and
the vendor's own statements. Section @sec:data describes the dataset, how it was collected and what it does
not cover. Section @sec:method states the identity, works it through for one product, and sets out the three
estimators and the seven hypotheses. Section @sec:results reports the results in the order of the research
questions: how fast the peaks grew, where the growth came from, how our split compares with NVIDIA's, how
efficiency and memory moved, and whether measured throughput followed the peaks. Section @sec:robust reports the
sensitivity analyses, and Sections @sec:discussion to @sec:conclusion discuss, qualify and conclude.

# Background {#sec:background}

**Moore, Dennard and Koomey.** Moore's 1965 paper projected the number of components per chip at minimum cost
[@moore1965]. In 1975 he split the growth of chip complexity into larger dies, finer dimensions and a residual of
"circuit and device cleverness", the first decomposition of this kind, and forecast the two-year cadence usually
quoted [@moore1975]. His own numbers are worth recalling, because the exercise below repeats them for a later
decade: from 1959 to 1975 he credited a factor of about 20 to chip area and about 32 to finer dimensions, which <!-- numbers-ok: quoted from the cited source -->
left a residual of about 100 for cleverness, and he expected that residual to be nearly exhausted, with "another <!-- numbers-ok: quoted from the cited source -->
factor of four" at most still to come [@moore1975]. Dennard and colleagues showed that shrinking
a MOSFET's dimensions and voltage together keeps power density constant [@dennard1974]; when voltage scaling
stalled in the mid-2000s, clock rates stopped rising and the gains from a new node had to be spent on more
cores or more specialised logic. Esmaeilzadeh and colleagues modelled the consequence, "dark silicon": under a
fixed power budget a growing fraction of a chip's transistors must be switched off, more than half of them at <!-- numbers-ok: quoted from the cited source -->
the 8 nm node in their projection [@esmaeilzadeh2011]. Koomey and colleagues measured the efficiency of <!-- numbers-ok: quoted from the cited source -->
computing, peak computations per kilowatt-hour, and found that it doubled every 1.57 years from 1946 to 2009 <!-- numbers-ok: quoted from the cited source -->
[@koomey2011]. Nagy and colleagues hindcast 62 technologies and found that an exponential trend in time forecasts <!-- numbers-ok: quoted from the cited source -->
nearly as well as Wright's law, while warning that short, noisy series fit it only loosely [@nagy2013]; a
fourteen-year panel of accelerators is such a series.

**Specialization as the successor to scaling.** Leiserson and colleagues argued that after Moore's law,
performance must come from "the Top" of the computing stack, software, algorithms and hardware architecture,
and that domain-specific hardware can run applications tens to hundreds of times faster by using fewer
transistors [@leiserson2020]. They also dated the end of the clock era: clock speed rose more than two
hundred-fold from 1985 to 2005 and then plateaued with the end of Dennard scaling, and they did not expect <!-- numbers-ok: quoted from the cited source -->
it to rise again. Thompson and colleagues showed that the computation used by deep learning grew far
faster than per-chip hardware, mostly by running models longer on more machines [@thompson2020limits]. Jouppi and colleagues documented Google's TPUs, the
clearest case of a domain-specific accelerator built for machine learning [@jouppi2017; @jouppi2023]. Khan and
Mann explained for a policy audience why such chips outperform general-purpose processors, by parallelism, low
precision, memory organisation and domain-specific languages, and put the advantage at ten to a thousand times <!-- numbers-ok: quoted from the cited source -->
for a given process node [@khan2020].

**Matrix instructions and number formats.** Two of the mechanisms in that list are the architectural terms of
our identity, and the vendor literature describes both. The first TPU was built around a matrix unit of 65,536 <!-- numbers-ok: quoted from the cited source -->
eight-bit multiply–accumulators with a peak of 92 TOPS at 700 MHz on a 28 nm process [@jouppi2017]. On the GPU <!-- numbers-ok: quoted from the cited source -->
side, Dally, Keckler and Kirk trace the same path: Kepler at 4 TFLOP/s of FP32, Pascal adding a 16-bit vector <!-- numbers-ok: quoted from the cited source -->
rate, Volta's HMMA matrix instruction at 125 TFLOP/s of FP16, Turing's IMMA at INT8 and Ampere's sparse matrix <!-- numbers-ok: quoted from the cited source -->
instructions [@dally2021micro]. Dally's Hot Chips keynote gives the energy reason a matrix instruction raises
the work done per transistor: instruction fetch, decode and operand fetch cost about twenty times the arithmetic <!-- numbers-ok: quoted from the cited source -->
of a scalar 16-bit fused multiply–add, but only about a fifth of the arithmetic of an HMMA and about a sixth of <!-- numbers-ok: quoted from the cited source -->
an IMMA, so a matrix instruction amortises the overhead over many multiply–accumulates [@dally2023hotchips].
Narrower formats are the other mechanism. Micikevicius and colleagues proposed the two FP8 encodings, E4M3 and
E5M2, with the stated aim of "smaller and more power efficient math pipelines" and lower memory bandwidth
pressure, and reported FP8 training that matched 16-bit results on models of up to 175 billion parameters <!-- numbers-ok: quoted from the cited source -->
[@micikevicius2022]. Each halving of the operand width lets the same arithmetic area do about twice the
operations per cycle, which is why the precision term of the identity moves in steps of one doubling.

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
data and found clock frequency to be the main driver of GPU FLOPS growth, measured at FP32 and base clock, with
GPU frequencies tripling from about 600 MHz to 1.8 GHz over their window and FLOPS per watt doubling every three <!-- numbers-ok: quoted from the cited source -->
to four years [@sun2019]. Epoch AI estimated that the FP32 price-performance of GPUs doubles about every 2.5 years <!-- numbers-ok: quoted from the cited source -->
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
production workloads on the first TPU were memory-bound, so that a chip with a peak of 92 TOPS delivered 21.4 on <!-- numbers-ok: quoted from the cited source -->
average [@jouppi2017], and split one TPU generation's peak gain
into more matrix units and a higher clock while memory bandwidth rose much less [@jouppi2023]. MLPerf provides measured training and inference throughput on fixed tasks [@mattson2020;
@reddi2020], which we use to check whether realized performance follows the headline peaks. Large training
runs report the same gap in another unit: Chowdhery and colleagues define model FLOPs utilization as observed
throughput over the throughput the vendor peak would allow, and tabulate values between about a fifth and a <!-- numbers-ok: quoted from the cited source -->
half for four large language models [@chowdhery2023].

# Data {#sec:data}

**Unit and population.** The unit is a product: a distinct silicon configuration sold or deployed as a data-centre
machine learning accelerator, announced between 2012 and 2026. Variants of the same silicon that differ in
memory, power or form factor are separate rows linked to a primary variant, the highest-TDP module form; only
primary variants enter the analyses. Throughput, bandwidth and transistors are counted per package. A board that
carries two packages is recorded as one package (NVIDIA's K80 as one of its two GK210 GPUs, Tenstorrent's
Wormhole n300 as its single-ASIC sibling n150), so that a product is compared with others on the same unit. The
dataset has {{population.products}} products from
{{population.vendors}} vendors, {{population.primary}} of them primary. Within each vendor and architecture
generation, the *flagship* is the primary part with the highest headline dense rate among parts positioned for
training; there are {{population.flagships}}. One card whose rates are given for an unstated number of chips is
excluded from every analysis.

**Fields.** For each product we record the announce and ship dates, process node and foundry, transistor count,
compute and total die area, number of compute dies, boost clock, TDP, memory capacity and bandwidth, and every
published peak rate: vector FP64, FP32, FP16, BF16 and INT8, and matrix-unit rates from FP64 down to FP4 and
INT4, dense and, separately, with structured sparsity. Vector and matrix-unit rates at the same precision are
separate columns, because the specialization term is meant to capture the matrix units. Prices are recorded
where a vendor publishes them; none does for the products in the sample, so no per-dollar analysis is possible.

**Collection.** The pre-registration lists a seed of products by name and an inclusion rule. For each product
the vendor's datasheet, whitepaper, product page or paper was opened and every value transcribed by hand with its
URL, the access date and a confidence level. Fifteen products beyond the seed were added because they met the
inclusion rule, and three were left out because no vendor document gives a peak rate; both lists are in the
deviations log. Values that a vendor states only indirectly are recorded as derived and carry the vendor's
sentence in their note: the main case is dense matrix rates given as half of the sparse rate where the vendor's
own page says so. Where two documents disagree, the vendor's datasheet wins and the alternatives are listed in
`data/conflicts.md`. A validator requires every value in the table to equal a row of the source table, so a
source cannot be present without matching the value it is supposed to support.

**Sources.** Every value carries a URL, an access date and a confidence level in `data/sources.csv`. The order of
preference is the vendor's datasheet, whitepaper or product page, then a vendor-authored paper, then Epoch AI's
hardware database [@epoch2026database] at medium confidence where the vendor is silent. Of the
{{population.source_rows|,}} source rows, {{population.source_confidence.high|,}} are high confidence,
{{population.source_confidence.medium}} medium and {{population.source_confidence.low}} low. The medium rows are
mostly boost clocks that NVIDIA states in no document we could find and that Epoch AI carries from a third-party
database; a sensitivity analysis drops every value below high confidence. Where sources
disagree, the vendor's document wins and the alternatives are listed in `data/conflicts.md`.

**Decisions taken during collection.** Four decisions were taken at review gates after the pre-registration was
frozen, each recorded in `DEVIATIONS.md` with its date, reason and effect. (i) Dense rates may be derived as half
of the published sparse rate where the vendor's own page states that rule; without it, H100, B200 and B300 would
enter the sample at their FP32 rates, because NVIDIA lists their tensor rates with sparsity only. (ii) Epoch AI's
database may supply a value at medium confidence where no vendor document gives it, because the pre-registered
fallback for clocks refused every automated request. (iii) Throughput is counted per package, which makes K40
rather than the two-GPU K80 the Kepler flagship, and the highest-TDP module is the primary variant, which makes
MI325X rather than MI300X the primary row of that silicon; a sensitivity analysis with MI300X as the primary
gives the same chain shares. (iv) A column for vector INT8 rates was added to the frozen schema, because the
headline is defined over every published format and AMD's MI60 publishes a vector INT8 rate twice its FP16
rate. None of these changes a definition or a decision rule.

**Coverage.** The decomposition needs five fields (transistor count, compute die area, clock, TDP and a reference
rate), and publication of these has declined. NVIDIA has not published die area or boost clock for Blackwell or
Rubin, AMD has not published die area since MI100, and Google publishes neither transistor count nor die area for
its TPUs. Only {{population.A_flagships}} flagships have all five fields; {{population.A_prime_flagships}} have
every field except die area and {{population.clock_free_flagships}} every field except the clock. We use the
last two groups with reduced identities (Section @sec:method). `data/coverage.md` lists, for every product, the
fields it lacks. Table @tbl:sample lists the {{population.A_flagships}} products of the decomposition sample
with their five inputs. They run from K40's {{sample[product=K40].headline_tflops|.1f}} TFLOP/s of vector FP32
to H100's {{sample[product=H100 SXM5 80GB].headline_tflops|,.0f}} TFLOP/s of FP8 matrix arithmetic, and include
one wafer-scale part, Cerebras' WSE-2, whose
{{sample[product=WSE-2].area_mm2|,.0f}} mm² and {{sample[product=WSE-2].transistors_b|,.0f}} billion transistors
are two orders of magnitude above the rest; it is kept in every fit and dropped in a sensitivity analysis.

: The decomposition sample: the {{population.A_flagships}} flagships that publish all five inputs of identity A, oldest first. $N$ transistors per package (billions), $A$ compute die area, $f$ boost clock, $W$ TDP, $R$ the dense reference rate and $P$ the headline dense rate, each with its format. Announce dates are decimal years. {#tbl:sample}

<!-- include: results/tables/t9_sample.md -->

**Measured throughput.** For the comparison of peaks with measured performance we collected MLPerf results for
NVIDIA's flagships from the published result tables, in `data/mlperf.csv` with the URL of each result. For
training, the metric is time to train to a fixed quality target [@mattson2020], and we convert it to a
per-accelerator throughput as the inverse of the product of training time and the number of accelerators in the
submitted system. For inference, we take the offline scenario, in which data are available in advance and an
accelerator can reach and hold its peak [@reddi2020], and divide the system's samples per second by its
accelerator count. For each product and benchmark the pre-registered rule takes the first round in which the
product appears, the result closest to launch software; the best result over all rounds is reported alongside.
Rows from a benchmark whose definition changed between rounds are kept in the file with the reason and left out
of the comparison.

**Process nodes.** To ask whether accelerators reach new nodes later than they used to, we also compiled, for
each foundry node in the dataset, the year in which the foundry's own statements put it into volume production,
and mapped each vendor's custom node name onto the foundry node it is derived from. The lag is the announce
year minus the middle of the volume-production year.

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
transistors go to caches, I/O or features that do not raise $R$. Sparsity is outside $P$. The identity holds in
any consistent units; we use millions of transistors per mm² for density, mm² for area, MHz for the clock and
TFLOP/s for the rates, so that the five factors multiply to $P$ in TFLOP/s without a constant.

**A worked example.** H100 SXM5 publishes {{sample[product=H100 SXM5 80GB].transistors_b|.0f}} billion
transistors on {{sample[product=H100 SXM5 80GB].area_mm2|,.0f}} mm² of compute die, a boost clock of
{{sample[product=H100 SXM5 80GB].boost_clock_mhz|,.0f}} MHz, a dense FP16 matrix rate of
{{sample[product=H100 SXM5 80GB].ref_tflops|,.1f}} TFLOP/s and a dense FP8 matrix rate of
{{sample[product=H100 SXM5 80GB].headline_tflops|,.0f}} TFLOP/s, its headline. Its density is therefore
{{sample[product=H100 SXM5 80GB].density_mtr_mm2|.1f}} million transistors per mm², its specialization
{{sample[product=H100 SXM5 80GB].spec_ops_per_mtransistor_cycle|.2f}} reference operations per million
transistors per cycle, and its precision multiplier {{sample[product=H100 SXM5 80GB].precision_multiplier|.0f}},
because FP8 is one halving below the 16-bit reference. In base-two logarithms the identity reads
{{sample[product=H100 SXM5 80GB].density_mtr_mm2|lg}} (density) +
{{sample[product=H100 SXM5 80GB].area_mm2|lg}} (area) + {{sample[product=H100 SXM5 80GB].boost_clock_mhz|lg}}
(clock) {{sample[product=H100 SXM5 80GB].spec_ops_per_transistor_cycle|lg}} (specialization) +
{{sample[product=H100 SXM5 80GB].precision_multiplier|lg}} (precision) =
{{sample[product=H100 SXM5 80GB].headline_tflops|lg}}, which is $\log_2$ of the headline rate. The
specialization term is a small number because a transistor does far less than one operation per cycle; what
matters is its change between products.

**Reading the terms.** Density is Moore's law in its scaling sense, and the product of density and area, the
transistor count, is Moore's law in its original sense [@moore1965]. The clock is the term Dennard scaling
drove and its end froze [@dennard1974; @leiserson2020]. Specialization and precision are Leiserson's "Top":
specialization is what the microarchitecture does with each transistor in each cycle, and rises with matrix
units, wider datapaths and a larger fraction of the die devoted to arithmetic; precision is the number of
operations a datapath does at the headline format relative to the 16-bit reference, and rises by one doubling
for each halving of the operand width. Because the terms multiply, shares are taken on the logarithmic scale:
the share of a term over an interval is its change in $\log_2$ divided by the change in $\log_2 P$. Shares sum
to one, and a share can be negative, as precision's is on the step from A100 to H100, whose headline format
widened from INT4 to FP8.

**Reduced identities.** Two reduced identities cover products with missing fields. Identity A′ merges density and
area into the transistor count, $\log_2 P = \log_2 N + \log_2 f + \log_2 (R/Nf) + \log_2 (P/R)$, for products
without a published die area; its transistor term is Moore's law in the original sense. The clock-free identity
merges the clock into specialization, which becomes reference operations per transistor per second, $R/N$, for
products without a published clock. Identity B splits $P$ into $P/W$ and $W$, throughput per watt and the power
budget, and identity C into $P/A$ and $A$, throughput per mm² and the silicon area; both are reported for the
NVIDIA chain.

**Estimator (a): the chain.** The chain links the first flagship of each NVIDIA architecture from K20X (Kepler)
onward: K20X, M40, P100, V100, A100 and H100, named in the pre-registration. For each step it reports the change
in each term's $\log_2$, in doublings, and for the whole chain each term's cumulative change and share. The chain
cannot be extended past H100 under identity A because NVIDIA publishes neither die area nor boost clock for
Blackwell or Rubin; identity B, which needs only TDP, is carried to B300. A second chain follows AMD's Instinct
flagships from MI60 under identity A′, because AMD has not published die area since MI100.

**Estimator (b): the regression.** For every flagship with all five fields we regress $\log_2$ of each term and
of $P$ on the decimal announce year by least squares. Because the identity is additive in logarithms and least
squares is linear, the five term slopes sum exactly to the slope of $P$, so the regression is a decomposition
of the cross-vendor trend in the same way the chain is a decomposition of one vendor's steps. The doubling time
of a series is the inverse of its slope. Uncertainty comes from a bootstrap over chips: products are resampled
with replacement, 2,000 times from a fixed seed, and the same resampled set is used for every series in a draw, <!-- numbers-ok: design constant -->
so that a contrast between slopes, such as specialization + precision − density for H3 or headline − bandwidth
for H5, is computed within each draw and its interval is the percentile interval of those differences.
Heteroscedasticity-robust (HC3) standard errors and the Theil–Sen slope are reported as checks. The same
estimator is run under identity A′ and the clock-free identity on the larger samples those identities allow.

**Estimator (c): the reconciliation.** NVIDIA's account of the same decade [@dally2023hotchips] multiplies four
factors, number representation, complex instructions, process and sparsity. We compute identity A from K20X to
H100 at the endpoint rates NVIDIA's chart uses, K20X's FP32 rate and H100's FP8 rate, drop sparsity from both
sides, and compare the physical part of the identity, density × area × clock, which is $N f$, with NVIDIA's
"process" factor, and its architectural part, specialization × precision, with NVIDIA's number representation ×
complex instructions. Because NVIDIA's number representation factor starts from FP32, the same comparison is
repeated with FP32 as every chip's reference rate.

**Hypotheses.** Seven hypotheses were pre-registered with decision rules; Table @tbl:hyp repeats the rules next
to the outcomes. In short:

- **H1**, speed: the flagship headline rate doubles in at most 1.5 years, with the upper bound of its interval below 2 years. <!-- numbers-ok: pre-registered threshold -->
- **H2**, Moore's law is the minority: density doubles in at least 2.5 years and supplies less than a third of the NVIDIA chain's gain. <!-- numbers-ok: pre-registered threshold -->
- **H3**, architecture outweighs density: specialization and precision together exceed density, in the chain's shares and in the regression, where the contrast's interval must exclude zero.
- **H4**, bigger silicon and more watts after 2020: on the NVIDIA chain, die area and TDP grow more per step after 2020 than before.
- **H5**, the memory wall: the headline slope exceeds the bandwidth slope and the interval of the difference excludes zero.
- **H6**, exploratory: per-accelerator MLPerf throughput grows more slowly than the headline rate on every benchmark with three generations.
- **H7**, the reconciliation: from K20X to H100, transistors × clock grew at least 10×, four times NVIDIA's process factor. <!-- numbers-ok: pre-registered threshold -->

**Pre-registration.** The question, the definitions, the sample rule, the estimators, the seven hypotheses with
their decision rules and the sensitivity analyses were frozen at the git tag `prereg-v1` before any value was
collected. The thresholds were set after the author had worked the identity through from remembered headline
figures, so the pre-registration is not blind. Every later change, including the four decisions taken at review
gates during data collection, is logged with its date and reason in `DEVIATIONS.md`; the main ones are
described where they matter below.

**Reproducibility.** Every number in this paper, in the text as well as in the tables, is filled from one results
file by the build, which fails if a number is typed by hand; `make all` regenerates the results file, the figures
and the paper from the committed dataset without network access. The released dataset carries the per-value
provenance described above, so a reader can check any input against the vendor's document.

# Results {#sec:results}

## How fast {#sec:rate}

Figure @fig:f1 shows the ladder. Over all {{rq1_throughput.flagships.headline.n}} flagships with a headline
rate, the headline doubled every {{rq1_throughput.flagships.headline.fit.doubling_years|.2f}} years (95% CI
{{rq1_throughput.flagships.headline.fit.doubling_ci[0]|.2f}}–{{rq1_throughput.flagships.headline.fit.doubling_ci[1]|.2f}}),
the 16-bit reference rate every {{rq1_throughput.flagships.ref_tflops.fit.doubling_years|.2f}} years and the
vector FP32 rate every {{rq1_throughput.flagships_ladder.fp32.fit.doubling_years|.2f}} years, slower than Epoch
AI's 2.3 years for the FP32 peak of machine learning hardware in general [@epoch2023hardware]. <!-- numbers-ok: quoted from the cited source --> The three
series are ordered as the identity predicts: the gap between the FP32 and the 16-bit trends is what matrix units
and 16-bit datapaths added, and the gap between the 16-bit and the headline trends is what narrower formats
added on top. The headline rate of a 2026 flagship is the same quantity as the FP32 rate of a 2013 flagship,
two operations per multiply–accumulate, but at a narrower precision and, for some products, over several dies.

The silicon behind the rates grew more slowly, and in a different way. Transistors per
package doubled every {{rq1_throughput.flagships.transistors_b.fit.doubling_years|.2f}} years over
{{rq1_throughput.flagships.transistors_b.n}} flagships (Figure @fig:f1(b)), close to Moore's
1975 cadence, but transistor density, over the {{rq1_throughput.flagships_density.density_mtr_mm2.n}} flagships
that publish both count and area, doubled only every
{{rq1_throughput.flagships_density.density_mtr_mm2.fit.doubling_years|.2f}} years (CI
{{rq1_throughput.flagships_density.density_mtr_mm2.fit.doubling_ci[0]|.2f}}–{{rq1_throughput.flagships_density.density_mtr_mm2.fit.doubling_ci[1]|.2f}}).
The difference is area. The compute die area of single-die flagships has been nearly flat since V100 at a little
over {{sample[product=V100 SXM2 16GB].area_mm2|,.0f}} mm², close to the lithographic reticle, so the
transistor count of a package now grows by putting more dies in it; the two wafer-scale parts sit two orders of
magnitude above that line (Figure @fig:f1(d)), which is why the area trend has the widest interval in the figure.
On the {{hypotheses.H1.n}} flagships with all five fields, the headline doubled every
{{hypotheses.H1.doubling|.2f}} years (CI {{hypotheses.H1.doubling_ci[0]|.2f}}–{{hypotheses.H1.doubling_ci[1]|.2f}}),
which meets H1. The headline rate has therefore doubled two to three times as fast as density, and the rest of
this section asks where the difference comes from.

![Flagships against announce year, log scale, with least-squares trends and 95% bootstrap intervals for the
doubling time. (a) Peak rates: headline dense (largest dense rate over all formats), 16-bit reference and vector
FP32; the legend gives each series' sample and doubling time. (b) Transistors per package, (c) transistor
density and (d) compute die area, with the sample and doubling time in each panel; these three panels use the
colours their terms carry in Figures @fig:f2, @fig:f3 and @fig:f7. Hollow markers: wafer-scale parts, which are
included in every fit. Each series is fitted on the flagships that publish
it.](results/figures/f1_ladder.svg){#fig:f1 width=100%}

## Where it comes from {#sec:decomp}

**The NVIDIA chain.** Figure @fig:f2 and Table @tbl:chain give the chain decomposition. From K20X to H100, density contributed
{{estimator_a.nvidia_a.cumulative.shares.density_mtr_mm2|.3f}} of the change in $\log_2 P$, die area
{{estimator_a.nvidia_a.cumulative.shares.area_mm2|.3f}}, clock {{estimator_a.nvidia_a.cumulative.shares.boost_clock_mhz|.3f}},
specialization {{estimator_a.nvidia_a.cumulative.shares.spec_ops_per_transistor_cycle|.3f}} and precision
{{estimator_a.nvidia_a.cumulative.shares.precision_multiplier|.3f}}. The steps differ in kind, and the table is
worth reading row by row. The Kepler-to-Maxwell step, {{estimator_a.nvidia_a.steps[0].dlog2_headline|.2f}}
doublings over three years on the same 28 nm node, came almost entirely from clock <!-- numbers-ok: node name -->
({{estimator_a.nvidia_a.steps[0].dlog2_boost_clock_mhz|.2f}} doublings). Maxwell to Pascal,
{{estimator_a.nvidia_a.steps[1].dlog2_headline|.2f}} doublings in less than half a year, is the chain's one large
density step ({{estimator_a.nvidia_a.steps[1].dlog2_density_mtr_mm2|.2f}} doublings, the move from 28 nm to <!-- numbers-ok: node names -->
16 nm FinFET), with a further clock gain and the first 16-bit vector rate. Pascal to Volta <!-- numbers-ok: node name -->
added tensor cores and raised specialization by {{estimator_a.nvidia_a.steps[2].dlog2_spec_ops_per_transistor_cycle|.2f}}
doublings in one step, the largest single-term change in the chain, while the die grew from
{{sample[product=P100 SXM2].area_mm2|,.0f}} to {{sample[product=V100 SXM2 16GB].area_mm2|,.0f}} mm². Volta to
Ampere took the headline to INT4, a precision gain of
{{estimator_a.nvidia_a.steps[3].dlog2_precision_multiplier|.2f}} doublings, on top of
{{estimator_a.nvidia_a.steps[3].dlog2_density_mtr_mm2|.2f}} doublings of density from the move to 7 nm; <!-- numbers-ok: node name -->
specialization barely moved on that step, because Ampere's 16-bit matrix rate rose
(from {{sample[product=V100 SXM2 16GB].ref_tflops|,.0f}} to {{sample[product=A100 SXM4 40GB].ref_tflops|,.0f}}
TFLOP/s) by about as much as its transistor count (from
{{sample[product=V100 SXM2 16GB].transistors_b|.1f}} to {{sample[product=A100 SXM4 40GB].transistors_b|.1f}}
billion). Hopper's headline format, FP8, is one step wider than Ampere's INT4, for which no H100 rate appears in
the documents we collected, so the precision term fell by
{{estimator_a.nvidia_a.steps[4].dlog2_precision_multiplier|.2f}} doublings in the last step and the headline
rose by only {{estimator_a.nvidia_a.steps[4].dlog2_headline|.2f}} doublings, although the 16-bit reference rate
itself rose from {{sample[product=A100 SXM4 40GB].ref_tflops|,.0f}} to
{{sample[product=H100 SXM5 80GB].ref_tflops|,.0f}} TFLOP/s on density, clock and specialization together. Die
area barely moved over the whole chain because K20X was already a large die.

: Estimator (a): the NVIDIA chain under identity A. Each row is one step of the chain; the entries are the change in $\log_2$ of each term, in doublings, and sum across the row to the change in the headline rate. The last two rows give the cumulative change and each term's share of it. {#tbl:chain}

<!-- include: results/tables/t3_chain_paper.md -->

**Transistors against density.** Over the chain the transistor count grew by
{{estimator_a.nvidia_a.cumulative.dlog2.transistors_b|.2f}} doublings, the sum of density's
{{estimator_a.nvidia_a.cumulative.dlog2.density_mtr_mm2|.2f}} and area's
{{estimator_a.nvidia_a.cumulative.dlog2.area_mm2|.2f}}. Under identity A′, which does not separate the two, the
transistor term takes {{estimator_a.nvidia_a_prime.cumulative.shares.transistors_mtr|pct}} of the NVIDIA chain,
and Moore's law in its original sense is a larger share of Huang's law than Moore's law in the scaling sense.
The distinction matters more after H100, when packages with several dies raise the count without raising the
density. AMD's Instinct chain from MI60 to MI355X, with identity A′ because AMD
does not publish die area, gives transistors {{estimator_a.amd_a_prime.cumulative.shares.transistors_mtr|.3f}},
clock {{estimator_a.amd_a_prime.cumulative.shares.boost_clock_mhz|.3f}}, specialization
{{estimator_a.amd_a_prime.cumulative.shares.spec_ops_per_transistor_cycle|.3f}} and precision
{{estimator_a.amd_a_prime.cumulative.shares.precision_multiplier|.3f}} of its
{{estimator_a.amd_a_prime.cumulative.dlog2_headline|.2f}} doublings in
{{estimator_a.amd_a_prime.cumulative.years|.1f}} years (Figure @fig:f2(b)). AMD's chain leans more on transistors
and less on clock than NVIDIA's, which is consistent with a line that moved to chiplet packages early, but the
two vendors agree that specialization is the largest architectural term and precision the smaller one.

![Chain-linked decomposition (estimator a). (a) Change in each term's $\log_2$ for each step of the NVIDIA chain,
identity A, as stacked bars; the dot is the net change in the headline rate, the sum of the bars, labelled in
doublings, and each step is labelled with its length in years. The steps from H100 onward cannot be
decomposed because NVIDIA does not publish die area or boost clock for Blackwell or Rubin. (b) Each term's share of
the cumulative change in $\log_2 P$: NVIDIA K20X → H100 (identity A) and AMD MI60 → MI355X (identity A′, where
transistors stand for density × area).](results/figures/f2_chain.svg){#fig:f2 width=100%}

**H2: Moore's law proper is the minority.** Density's share of the NVIDIA chain,
{{hypotheses.H2.b_density_share|.3f}}, is below one third, and its doubling time across flagships,
{{hypotheses.H2.a_density_doubling|.2f}} years, is above 2.5 years, so H2 is supported. <!-- numbers-ok: pre-registered thresholds --> The
margin is thin: a change of {{hypotheses.H2.b_margin_endpoint_change|pct1}} in the transistor count or die
area of either endpoint would move the share to one third. Vendor transistor counts are rounded figures, so
the honest statement is that density's share is about a third, not that it is below one.

**H3: architecture and arithmetic outweigh density.** In the chain, specialization and precision together
account for {{hypotheses.H3.a_arch_share|.3f}} of the gain against density's {{hypotheses.H3.a_density_share|.3f}},
so part (a) holds. The regression (Table @tbl:trend, Figure @fig:f3) tells a less clear story. Across the nine
flagships, density rose at {{estimator_b.fits.density_mtr_mm2.slope|.3f}} doublings per year with the narrowest
interval of any term, specialization at {{estimator_b.fits.spec_ops_per_transistor_cycle.slope|.3f}}, precision
at {{estimator_b.fits.precision_multiplier.slope|.3f}} with an interval that touches zero, and the clock at
{{estimator_b.fits.boost_clock_mhz.slope|.3f}}; area's slope, {{estimator_b.fits.area_mm2.slope|.3f}}, is pulled
up by the wafer-scale part and has the widest interval. The specialization and precision slopes
sum to more than the density slope by {{hypotheses.H3.b_contrast.estimate|.3f}} doublings per year, but the
95% interval runs from {{hypotheses.H3.b_contrast.ci[0]|.3f}} to {{hypotheses.H3.b_contrast.ci[1]|.3f}}, and the
Theil–Sen version of the contrast is {{estimator_b.theil_sen_arch_minus_density|.3f}}. Part (b)
fails and H3 is falsified as pre-registered. With nine products, the regression cannot separate the
architectural terms from density, even though the chain puts them ahead; the two estimators do not contradict
each other, because the chain measures one vendor's path and the regression a cross-vendor trend whose nine
points include two parts, GC200 and WSE-2, with very different mixes of the terms.

: Estimator (b): trends of identity A's terms over the {{estimator_b.n}} flagships with all five fields (K40, M40, P100, V100, MI60, A100, GC200, WSE-2, H100). Slopes in doublings per year with 95% bootstrap intervals; the term slopes add up to the headline slope. {#tbl:trend}

| term | slope (doublings/yr) | 95% CI | doubling time (yr) |
|---|---|---|---|
| headline rate $P$ | {{estimator_b.fits.headline.slope\|.3f}} | [{{estimator_b.fits.headline.slope_ci[0]\|.3f}}, {{estimator_b.fits.headline.slope_ci[1]\|.3f}}] | {{estimator_b.fits.headline.doubling_years\|.2f}} |
| density $N/A$ | {{estimator_b.fits.density_mtr_mm2.slope\|.3f}} | [{{estimator_b.fits.density_mtr_mm2.slope_ci[0]\|.3f}}, {{estimator_b.fits.density_mtr_mm2.slope_ci[1]\|.3f}}] | {{estimator_b.fits.density_mtr_mm2.doubling_years\|.2f}} |
| area $A$ | {{estimator_b.fits.area_mm2.slope\|.3f}} | [{{estimator_b.fits.area_mm2.slope_ci[0]\|.3f}}, {{estimator_b.fits.area_mm2.slope_ci[1]\|.3f}}] | {{estimator_b.fits.area_mm2.doubling_years\|.2f}} |
| clock $f$ | {{estimator_b.fits.boost_clock_mhz.slope\|.3f}} | [{{estimator_b.fits.boost_clock_mhz.slope_ci[0]\|.3f}}, {{estimator_b.fits.boost_clock_mhz.slope_ci[1]\|.3f}}] | {{estimator_b.fits.boost_clock_mhz.doubling_years\|.2f}} |
| specialization $R/(Nf)$ | {{estimator_b.fits.spec_ops_per_transistor_cycle.slope\|.3f}} | [{{estimator_b.fits.spec_ops_per_transistor_cycle.slope_ci[0]\|.3f}}, {{estimator_b.fits.spec_ops_per_transistor_cycle.slope_ci[1]\|.3f}}] | {{estimator_b.fits.spec_ops_per_transistor_cycle.doubling_years\|.2f}} |
| precision $P/R$ | {{estimator_b.fits.precision_multiplier.slope\|.3f}} | [{{estimator_b.fits.precision_multiplier.slope_ci[0]\|.3f}}, {{estimator_b.fits.precision_multiplier.slope_ci[1]\|.3f}}] | {{estimator_b.fits.precision_multiplier.doubling_years\|.2f}} |

![Regression decomposition (estimator b). (a) Trend of each term, in doublings per year, with 95% bootstrap
intervals, for identity A and the two reduced identities on the flagships each covers; under the clock-free
identity the clock is part of specialization, and under identity A′ density and area are one transistor term.
(b) The H3b contrast, specialization + precision − density, under each sensitivity analysis of Table @tbl:sens;
blue: the primary analysis; orange: intervals that exclude zero.](results/figures/f3_regression.svg){#fig:f3 width=100%}

**H4: bigger silicon and more watts.** After 2020 the chain has a single step that can be decomposed, A100 to
H100. On it, TDP grew by {{hypotheses.H4.mean_dlog2_tdp_w_late|.2f}} doublings against a mean of
{{hypotheses.H4.mean_dlog2_tdp_w_early|.2f}} on earlier steps, but die area shrank by
{{hypotheses.H4.mean_dlog2_area_mm2_late|.2f}} doublings against an earlier mean of
{{hypotheses.H4.mean_dlog2_area_mm2_early|.2f}}, so H4 is not supported. Area growth after H100 has come from
putting two dies in a package, which NVIDIA has not quantified. TDP alone, over the full chain to B300, grew by
{{hypotheses.H4.supplementary_tdp_full_chain.mean_dlog2_tdp_w_late|.2f}} doublings per step after 2020 against
{{hypotheses.H4.supplementary_tdp_full_chain.mean_dlog2_tdp_w_early|.2f}} before. In identity B over the same
chain, the power budget accounts for {{estimator_a.nvidia_b.cumulative.shares.tdp_w|.3f}} of the gain and
efficiency for {{estimator_a.nvidia_b.cumulative.shares.tflops_per_w|.3f}}: most of Huang's law is more work
per watt, but a fifth of it is more watts.

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
against NVIDIA's {{estimator_c.nvidia.non_physical|x0}}. Because the two totals agree, the factor that moves
between the physical and the architectural columns is the same on both sides, about
{{estimator_c.physical_over_nvidia_process|.0f}}×: what NVIDIA's account adds to architecture, it takes from
process.

The two accountings differ in bookkeeping. NVIDIA's "process" is the gain per transistor from a newer node;
the extra transistors that the node and a larger die make available are credited to the architecture that uses
them. Identity A counts every transistor as a physical input and credits architecture only with what it does
per transistor per cycle. Neither is wrong, but they answer different questions: NVIDIA's says what the design
team did with the transistors it was given; ours says how much of the gain would have arrived without any change
in what a transistor does. The correspondence between the architectural terms is closer than the totals
suggest. NVIDIA's "complex instructions" are the matrix instructions whose per-operation overhead Dally's own
energy figures describe (Section @sec:background); those instructions are what raises our specialization term,
operations per transistor per cycle at the reference precision. NVIDIA's "number representation" runs from
FP32 to FP8 and so contains the move to 16-bit formats, which in our identity is part of the reference rate and
hence of specialization, not of precision. Taking FP32 as the reference for every chip, which is closer to
NVIDIA's "number representation", moves most of the architectural gain from specialization to precision
({{estimator_c_fp32_reference.factors.precision_multiplier|x1}} precision and
{{estimator_c_fp32_reference.factors.spec_ops_per_transistor_cycle|x2}} specialization, below one because an
FP32 operation on H100's matrix units costs more transistor-cycles than an FP32 operation on K20X's vector
units) but leaves the physical factor where it was. The choice of reference rate therefore moves gain between
the two architectural terms and never between architecture and physics.

![NVIDIA's account of K20X → H100 against identity A, as segments of $\log_2$ of the gain, each labelled with its
factor. Top: Dally's four factors [@dally2023hotchips]; sparsity (hatched) is outside the dense comparison.
Middle: identity A with the 16-bit reference. Bottom: identity A with FP32 as every chip's reference, where
specialization falls below one and is drawn left of zero. The dashed line marks the dense total. Colours pair
each of NVIDIA's factors with its nearest counterpart in the identity (process with density, complex
instructions with specialization, number representation with precision); die area and clock have no
counterpart in NVIDIA's account. The physical factors (density, area, clock) multiply to
{{estimator_c.physical_nf|x1}}, against {{estimator_c.nvidia.process|x1}} for
process.](results/figures/f7_dally.svg){#fig:f7 width=100%}

: Estimator (c): identity A from K20X to H100 SXM against NVIDIA's account. The FP32-reference column applies the FP32 sensitivity of Section @sec:robust. {#tbl:recon}

<!-- include: results/tables/t4_reconciliation.md -->

## Efficiency and memory {#sec:mem}

Figure @fig:f4 shows three efficiency ratios. Headline throughput per watt of TDP doubled every
{{rq3_efficiency.tflops_per_w.fit.doubling_years|.2f}} years over {{rq3_efficiency.tflops_per_w.n}} flagships,
the 16-bit reference rate per watt every {{rq3_efficiency.ref_tflops_per_w.fit.doubling_years|.2f}} years,
throughput per mm² of compute die every {{rq3_efficiency.tflops_per_mm2.fit.doubling_years|.2f}} years and per
billion transistors every {{rq3_efficiency.tflops_per_btransistor.fit.doubling_years|.2f}} years. Koomey's
efficiency trend for general computing was a doubling every 1.57 years [@koomey2011]; <!-- numbers-ok: quoted from the cited source --> peak AI throughput per
watt has kept a similar pace, mostly through formats and matrix units rather than voltage. The gap between the
headline and the reference rate per watt, {{rq3_efficiency.tflops_per_w.fit.doubling_years|.2f}} against
{{rq3_efficiency.ref_tflops_per_w.fit.doubling_years|.2f}} years, is the precision term again: at a fixed
format, efficiency has improved at about the pace Epoch AI reports for FP32 FLOP/s per watt, a doubling every
3.0 years [@epoch2023hardware], and the faster headline figure comes from doing the arithmetic at narrower <!-- numbers-ok: quoted from the cited source -->
widths. Throughput per mm² doubles almost as fast as throughput itself, because the area of a single die has
stopped growing; throughput per transistor, which is specialization × precision × clock, doubles every
{{rq3_efficiency.tflops_per_btransistor.fit.doubling_years|.2f}} years and is the cleanest cross-vendor measure
of how much more each transistor does.

![Efficiency of flagships: headline rate (a) per watt of TDP, (b) per mm² of compute die and (c) per billion
transistors, log scale, with least-squares trends and 95% bootstrap intervals; hollow markers are wafer-scale
parts. No vendor publishes prices for these products, so no per-dollar series is
shown.](results/figures/f4_efficiency.svg){#fig:f4 width=100%}

Memory has not kept up (Figure @fig:f5). Over {{rq4_memory.mem_bandwidth_gbs.n}} flagships, bandwidth doubled
every {{rq4_memory.mem_bandwidth_gbs.fit.doubling_years|.2f}} years and capacity every
{{rq4_memory.mem_capacity_gb.fit.doubling_years|.2f}} years, while the headline rate doubled every
{{rq4_memory.headline.fit.doubling_years|.2f}} years, so the operations available per byte fetched doubled every
{{rq4_memory.ops_per_byte.fit.doubling_years|.2f}} years (fitted directly to the ratio on the flagships that
report bandwidth, so it is not exactly the difference of the two slopes). In Figure @fig:f5(a) the flagships climb
from the line of about twenty operations per byte, where K40 sits, to about a thousand for the newest parts,
near the ridge point of 1,350 operations per byte that Jouppi and colleagues reported for the first TPU's roofline <!-- numbers-ok: quoted from the cited source -->
[@jouppi2017]; a workload whose arithmetic intensity is below a chip's ratio is bandwidth-bound on it, and the
figure shows the whole industry moving that ratio up. Expressed per two years, the unit Gholami and colleagues use, the headline rate grew
{{per_two_years.headline|x2}} and bandwidth {{per_two_years.mem_bandwidth_gbs|x2}}, against their 3.0× and 1.6× <!-- numbers-ok: quoted from the cited source -->
for server hardware since 1998 [@gholami2024]; their series is broader and longer than ours, so the two are <!-- numbers-ok: quoted from the cited source -->
independent estimates that agree rather than a replication. Flagship bandwidth grew faster than the four-year
doubling Epoch AI found for machine learning hardware in general [@epoch2023hardware], <!-- numbers-ok: quoted from the cited source -->
but not as fast as compute. In the pre-registered test on the decomposition sample
(n = {{hypotheses.H5.n}}), the headline slope exceeds the bandwidth slope by {{hypotheses.H5.contrast.estimate|.3f}}
doublings per year (CI {{hypotheses.H5.contrast.ci[0]|.3f}}–{{hypotheses.H5.contrast.ci[1]|.3f}}), so H5 is
supported; on all {{hypotheses.H5.all_flagships.n}} flagships with both, the gap is
{{hypotheses.H5.all_flagships.contrast.estimate|.3f}} ({{hypotheses.H5.all_flagships.contrast.ci[0]|.3f}}–{{hypotheses.H5.all_flagships.contrast.ci[1]|.3f}}).

![Memory wall. (a) Headline dense rate against memory bandwidth for flagships, coloured by announce period;
grey lines: constant operations per byte; the earliest product (K40) and the product with the largest headline
rate (MI455X) are labelled. (b) Headline operations per byte of bandwidth against announce year, with
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
{{hypotheses.H6.benchmarks[suite=inference].slope_headline|.2f}}. The gap is widest on ResNet-50 training, the
oldest benchmark, whose V100-to-H100 span includes the precision steps that raised the headline without raising
the rate at which a 16-bit training job runs, and narrowest on offline inference, the scenario that Reddi and
colleagues describe as the one in which an accelerator can hold its peak [@reddi2020]. Taking each product's
best result over all rounds instead of its first gives the same verdict on every benchmark
({{hypotheses.H6.best_rule.benchmarks[benchmark=bert].slope_realized|.2f}} doublings per year on BERT, for
example). H6 was pre-registered as exploratory. With three
products per benchmark, results from systems of different sizes and software of different ages, and the BERT
results of the first round excluded because that round's accuracy target was lower, it is a consistency check and
not an estimate of the gap. Software moves these results too: between the first two training rounds, the best
16-chip results improved 1.3× on unchanged hardware [@mattson2020], so a first-round result understates what <!-- numbers-ok: quoted from the cited source -->
the same chip delivers later; Google measured larger compiler-only gains over 20 months on both GPUs and TPUs <!-- numbers-ok: quoted from the cited source -->
[@jouppi2021]. Since those gains accrue to the measured series and not to the headline, the direction of the
result is conservative: the measured series grows more slowly than the peaks even with the software gains on its
side.

![Peak against measured, NVIDIA flagships. Doublings since the first product of each benchmark, by announce
year, for the headline dense rate and for per-accelerator MLPerf throughput (the first result for each product;
training: inverse time to train per accelerator); the ticks name each product and its announce year, and the
two slopes in doublings per year are printed in each panel. (a) BERT training, (b) Llama 2 70B LoRA fine-tuning,
(c) ResNet-50 training, (d) Llama 2 70B inference, offline scenario.](results/figures/f6_mlperf.svg){#fig:f6 width=100%}

## Hypotheses

Table @tbl:hyp collects the seven decisions. Five hypotheses are supported, one is not supported and one is
falsified; the two failures are reported with the same weight as the successes, as the pre-registration requires.

: Pre-registered hypotheses, decision rules and outcomes. CIs are 95% bootstrap intervals. {#tbl:hyp}

<!-- include: results/tables/t1_hypotheses.md -->

# Robustness {#sec:robust}

The pre-registered sensitivity analyses rerun estimator (b) under a changed definition or a changed sample.
Table @tbl:sens gives the short form, with the headline doubling time, the density doubling time and the H3b
contrast of each variant; the full table with every term is in the repository
(`results/tables/t5_sensitivity.md`), and Figure @fig:f3(b) shows the H3b contrast under each of them. H1 holds
in every variant that can be computed:
the headline doubling time ranges from {{sensitivity[label=headline with sparsity].headline_doubling|.2f}} years
with sparsity to {{sensitivity[label=identity A′ (no area)].headline_doubling|.2f}} years with identity A′, and
is {{sensitivity[label=without NVIDIA].headline_doubling|.2f}} years without NVIDIA, on only
{{sensitivity[label=without NVIDIA].n}} products. Density's doubling time stays between
{{sensitivity[label=without wafer-scale].density_doubling|.2f}} and {{sensitivity[label=frontier envelope].density_doubling|.2f}}
years, apart from the same three-product sample ({{sensitivity[label=without NVIDIA].density_doubling|.2f}}).
Dropping every value below high confidence, which removes the Epoch AI clocks, leaves the headline doubling at
{{sensitivity[label=high-confidence values only].headline_doubling|.2f}} years on
{{sensitivity[label=high-confidence values only].n}} products. Counting I/O dies in the area changes nothing,
because no product in the decomposition sample has a separate I/O die.
The H3b contrast is positive in all but one variant, but its interval excludes zero only with FP32 as the
reference, with sparsity in the headline, and with vendor fixed effects over all products in the sample; each of
these changes either the definition or the sample, and none was the primary analysis. The first two are
instructive: with FP32 as the reference, the move to 16-bit formats counts as precision rather than as part of
the reference, and with sparsity in the headline the last two NVIDIA steps gain a doubling each; both raise the
architectural slopes rather than lowering density's.

: Sensitivity analyses, short form. $P$ doubling: the headline doubling time with its 95% bootstrap interval; density doubling: the density doubling time; H3b contrast: specialization + precision − density in doublings per year. The ship-date variant cannot be computed because only two of the nine products in the decomposition sample publish a ship date. The full table is `results/tables/t5_sensitivity.md`. {#tbl:sens}

<!-- include: results/tables/t5_sensitivity_paper.md -->

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

# Discussion {#sec:discussion}

**Against other estimates.** The headline doubling time of about a year sits where the earlier literature put
it: Huang's 25× in five years [@perry2018spectrum] and Dally's 317× in eight [@dally2021micro] are both close to <!-- numbers-ok: quoted from the cited sources -->
a doubling a year, and our {{rq1_throughput.flagships.headline.fit.doubling_years|.2f}} years across vendors or
{{hypotheses.H1.doubling|.2f}} years on the decomposition sample confirm them on sourced data. The FP32 series is
the one comparable with the general trend studies, and it is slower: {{rq1_throughput.flagships_ladder.fp32.fit.doubling_years|.2f}}
years against Epoch AI's 2.3 years [@epoch2023hardware], which is expected for flagships that have moved their <!-- numbers-ok: quoted from the cited source -->
arithmetic to narrower formats and no longer grow their FP32 datapaths. Sun and colleagues found frequency to be
the main driver of GPU FLOPS since 2000 [@sun2019]; over our decade the clock still multiplied NVIDIA's
headline by {{estimator_c.clock_ratio|x1}}, a sixth of the chain's gain, but its cross-vendor trend,
{{estimator_b.fits.boost_clock_mhz.slope|.2f}} doublings per year, says that the era they describe was ending as
our window opened. On memory, our per-two-year factors, {{per_two_years.headline|x2}} for compute and
{{per_two_years.mem_bandwidth_gbs|x2}} for bandwidth, agree with Gholami and colleagues' 3.0× and 1.6× <!-- numbers-ok: quoted from the cited source -->
[@gholami2024] to within their rounding; our capacity figure, {{per_two_years.mem_capacity_gb|x2}} per two
years, is below the 2× they give for single-GPU memory. Khan and Mann's ten-to-a-thousand-fold advantage of AI <!-- numbers-ok: quoted from the cited source -->
chips over CPUs at a given node [@khan2020] is a comparison across chip types; the within-line counterpart here
is the {{estimator_c.architecture_spec_x_precision|x1}} that specialization and precision together added to
NVIDIA's flagship over a decade at the same vendor.

**Moore's own decomposition, fifty years on.** Moore's 1975 split of the previous sixteen years gave the
residual, "circuit and device cleverness", the largest share, about 100× against about 32× for finer dimensions <!-- numbers-ok: quoted from the cited source -->
and about 20× for area, and he expected that residual to run out [@moore1975]. Our split of 2012–2022 for <!-- numbers-ok: quoted from the cited source -->
accelerators has the same shape: the terms that are not density or area, clock, specialization and precision,
multiply to more than density and area do, and one of them, precision, has a visible floor. The difference is
that Moore's residual was a correction to a density forecast, whereas for accelerators the residual is the
larger part of the trend that is being forecast.

**What is left.** The terms of identity A have different futures. Density is the slow, steady term. The clock
has nearly stopped: its trend across flagships is {{estimator_b.fits.boost_clock_mhz.slope|.2f}} doublings per
year. Precision moves in single steps, and they run out: 8-bit floating-point formats for deep learning
[@micikevicius2022] reached the headline with Hopper, and four-bit formats with Blackwell. Each halving of the operand width at most doubles the
peak rate, and the headline formats of current flagships are four bits wide, so at most one or two such steps
remain before arithmetic reaches two bits or one. The area of a single die is bounded by the lithographic reticle,
which H100 already approaches; growth since then has come from packages with more than one die, which raises
the transistor count and, by identity B, power. Specialization has been the largest term after density, and
it is the one with no obvious bound, though its decade was dominated by a single invention, the matrix unit at
16-bit precision, and the chain shows it arriving in one step rather than along a trend.

**What this means for forecasts.** A forecast that extrapolates the headline doubling time of about a year
assumes that the non-density terms keep contributing as they did. Two of them, precision and clock, cannot
contribute at that rate for long, and a third, single-die area, is near its limit. If density keeps doubling
every two to three years and specialization keeps its pace, the headline rate would double more slowly than
in 2012–2022, unless packaging and power budgets keep growing. This is an argument about the composition of the
trend, not a forecast; our data do not identify a break. They also show that the headline rate overstates the
growth of measured throughput (Section @sec:mlperf), and that the memory system falls further behind every
year (Section @sec:mem). A forecast of delivered AI compute should therefore extrapolate the measured series,
or the 16-bit reference rate, rather than the headline, and should carry the memory trend alongside.

**Disclosure.** The most practical finding may be the coverage problem. In 2012–2020 NVIDIA published transistor
count, die area and clock for every flagship. For Blackwell and Rubin it publishes transistor counts but neither
die area nor boost clock, and other vendors publish less: AMD has given no die area since MI100 and Google no
transistor count or die area for any TPU. An exact accounting of where AI hardware gains come
from will soon be impossible from public documents unless vendors publish these five fields again. The reduced
identities soften the problem but do not solve it: identity A′ cannot separate density from area, and the
clock-free identity cannot separate the clock from architecture.

# Limitations {#sec:limits}

**Peaks are not performance.** The rates are vendor-published peaks, not measured throughput; Section @sec:mlperf shows that the two diverge.
Large training runs report a model FLOPs utilization of about 21–46% of the same peaks [@chowdhery2023], so a <!-- numbers-ok: quoted from the cited source -->
doubling of peak need not double delivered work. Our decomposition explains the number on the datasheet, which
is the number Huang's law is about, and not the work a chip does.

**Definitions vary across vendors.** Vendors define peak rates in slightly different ways (boost or sustained
clock, with or without the sparsity factor), and we took them as published, recording derived values as such.
The boost clock is the clock NVIDIA states its peaks at; where a vendor publishes one clock we used it, and the
{{population.source_confidence.medium}} medium-confidence values, mostly clocks from Epoch AI's database, are
dropped in one sensitivity analysis without changing the conclusions. The choice of the 16-bit reference rate
moves gain between specialization and precision (Table @tbl:recon) and does not move the physical factor; a
reader who prefers FP32 as the baseline should read the two architectural terms together.

**The sample is small and one vendor dominates it.** The decomposition sample is
{{population.A_flagships}} flagships, {{sensitivity[label=NVIDIA only].n}} of them NVIDIA's, and it ends in 2022;
the chain is one vendor's product line, frozen by name in the pre-registration. The intervals reflect sampling
over chips, not the measurement error in vendor figures, which are rounded. TPU and most post-2022 products enter
only the throughput, efficiency and memory trends. The regression's failure to separate the architectural terms
from density (H3b) is a failure to detect, not evidence of absence.

**Dates and prices.** Announce dates are the primary dates because ship dates are published for few products;
the two give similar doubling times where both exist. No vendor
publishes prices, so we could not compare performance per dollar with Epoch AI's estimates [@hobbhahn2022gpu],
and the identity says nothing about the cost of a transistor, a package or a watt.

**The pre-registration was not blind.** The author knew the headline figures of NVIDIA's flagships when setting the
thresholds. Two decision rules were close (H2b and the ship-date variant), and H2b's margin is within the
rounding of vendor transistor counts. The MLPerf comparison uses three products per benchmark and one vendor,
with systems of different sizes and software of different ages; it checks a direction and does not measure a gap.

# Conclusion {#sec:conclusion}

From 2012 to 2022, the vendor-published peak throughput of AI accelerators doubled about every year, and
transistor density, Moore's law in its scaling sense, supplied about a third of that growth. The rest came mostly
from specialization at 16-bit precision, then from clock and narrower formats, with die area contributing
little. NVIDIA's own account of the same decade agrees in total; it differs in counting the extra transistors as
architecture. Huang's law is therefore not Moore's law, but neither is it independent of it: without density,
the decade's gain would have been about a third smaller on a log scale, and without the transistors that density
and area together supplied, about two fifths smaller. Whether the next decade looks the same
depends on terms that the vendors have stopped publishing.

# Data and code availability {-}

The dataset (`data/accelerators.csv`, `data/sources.csv`), the pre-registration, the deviations log and the code
that produces every number, table and figure in this paper are released under CC BY 4.0 (data) and MIT (code)
at `https://github.com/thanatchon36/chipledger`, archived on Zenodo (doi:10.5281/zenodo.23763729, concept DOI) <!-- numbers-ok: DOI -->
and mirrored as a Hugging Face dataset (`thanatchon36/chipledger`). `make all` rebuilds the analysis from the
committed dataset without network access.

# References {-}

::: {#refs}
:::
