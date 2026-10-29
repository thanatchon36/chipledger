# LinkedIn drafts (not posted)

Numbers match `results/numbers.json` at the commit that adds this file. Keep "headline peak" or "vendor-published
peak"; never "performance" without that qualifier, because the paper's rates are datasheet peaks, not measured
throughput. Variant D is the launch post; it goes with `poster.png` (1200×1500, built by `scripts/poster.py`
from the same `numbers.json`). LinkedIn shows about the first 210 characters before "…more", so the hook is the
first three lines; links go in the first comment, where they do not cost reach.

Links: paper <https://thanatchon36.github.io/chipledger/paper/> · code and data
<https://github.com/thanatchon36/chipledger> · dataset <https://huggingface.co/datasets/thanatchon36/chipledger>
· DOI <https://doi.org/10.5281/zenodo.23763729>.

---

## Variant D: launch post (with `poster.png`)

NVIDIA's flagship AI chip got 501× faster on paper in ten years.

Its transistor count grew 11×. Its clock, 2.7×.

Where did the rest come from? I pre-registered a study and did the arithmetic.

"Huang's law" is the claim that AI chips outrun Moore's law. I wanted to know how much of it is Moore's law in
disguise. So I built a dataset of 79 data-centre AI accelerators from 14 vendors (2012–2026): 1,152 values,
each with a source URL, an access date and a confidence level. Then I split every vendor's published peak
into five factors that multiply exactly:

transistor density × die area × clock × operations per transistor per cycle (specialization) × the gain from
narrower number formats (precision).

No model, no residual. An accounting identity, true for every chip by construction.

What the data say:

→ The flagship headline peak doubled every 0.83 years from 2012 to 2022 (95% CI 0.62–1.13), and every 1.23
years over all 43 flagships to 2026. Moore's 1975 forecast for transistor counts was two years.

→ On NVIDIA's chain K20X → H100, the 501× splits into transistor density 33%, die area 6%, clock 16%,
specialization 34% and precision 11% of the log gain. Moore's law in the density sense is about a third of
Huang's law. The largest single term is the matrix units.

→ NVIDIA's own account (Dally, Hot Chips 2023) credits process with 2.5× and architecture with 200×. Same
total, different bookkeeping: transistors × clock grew 30.5×, 12 times NVIDIA's process factor, because NVIDIA
counts the extra transistors a new node gives as architecture. Where the gain "comes from" depends on who gets
credit for a transistor.

→ The memory wall is real and widening: memory bandwidth doubled every 2.70 years against 1.23 for compute, so
the operations a chip can do per byte it fetches double every 2.20 years.

→ A peak is not delivered work: on all four MLPerf benchmarks I could follow across NVIDIA generations, measured
per-accelerator throughput grew more slowly than the headline (ResNet-50 training: 0.45 vs 0.85 doublings per
year).

→ Disclosure ended in 2022. Since H100, no vendor in the sample publishes both die area and clock for its
flagship. From public documents, this decomposition cannot be done for Blackwell, Rubin, MI355X or any TPU.

Two caveats that belong on every chart:
1. Every rate is a vendor-published peak, dense, without sparsity. Peaks are what Huang's law is about, but they
are not what a training job gets.
2. The decomposition sample is 9 flagships, 6 of them NVIDIA's. Across vendors, the regression cannot separate
the architectural terms from density; that pre-registered hypothesis was falsified.

Of 7 pre-registered hypotheses: 5 supported, 1 not supported, 1 falsified. The ones that failed are in the
paper, with the same weight as the ones that passed.

Everything is open: the dataset with per-value provenance (CC BY 4.0), the code (MIT), the pre-registration
frozen in git before any value was collected, the deviations log and the paper. One command rebuilds every
number, figure and the PDF from the committed data, with no network.

Independent personal research. Public data only. Does not represent the views of any employer or institution.

#AI #Semiconductors #MooresLaw #GPU #HardwareEngineering #OpenData #Research

First comment:
📄 Paper: https://thanatchon36.github.io/chipledger/paper/
💻 Code and data: https://github.com/thanatchon36/chipledger
🤗 Dataset: https://huggingface.co/datasets/thanatchon36/chipledger
🔗 DOI: https://doi.org/10.5281/zenodo.23763729

---

## Variant D, Thai

ชิป AI เรือธงของ NVIDIA เร็วขึ้น 501 เท่าบนกระดาษในสิบปี

จำนวนทรานซิสเตอร์เพิ่ม 11 เท่า สัญญาณนาฬิกา 2.7 เท่า

แล้วที่เหลือมาจากไหน? ผมลงทะเบียนแบบวิจัยไว้ล่วงหน้า แล้วนั่งทำเลขคณิต

"กฎของ Huang" คือคำกล่าวว่าชิป AI โตเร็วกว่ากฎของ Moore ผมอยากรู้ว่ามันคือกฎของ Moore ที่แปลงร่างมามากแค่ไหน
จึงสร้างชุดข้อมูลของตัวเร่ง AI สำหรับศูนย์ข้อมูล 79 รุ่นจาก 14 ผู้ผลิต (2012–2026) รวม 1,152 ค่า ทุกค่ามี URL
ของแหล่งที่มา วันที่เข้าถึง และระดับความเชื่อมั่น แล้วแยกค่า peak ที่ผู้ผลิตประกาศออกเป็นห้าปัจจัยที่คูณกันพอดี:

ความหนาแน่นทรานซิสเตอร์ × พื้นที่ die × สัญญาณนาฬิกา × จำนวน operation ต่อทรานซิสเตอร์ต่อรอบ (specialization)
× กำไรจากรูปแบบตัวเลขที่แคบลง (precision)

ไม่มีโมเดล ไม่มีเศษเหลือ เป็นอัตลักษณ์ทางบัญชีที่จริงสำหรับทุกชิปโดยนิยาม

ข้อมูลบอกอะไร:

→ ค่า peak ของชิปเรือธงเพิ่มเป็นสองเท่าทุก 0.83 ปี ในช่วง 2012–2022 (95% CI 0.62–1.13) และทุก 1.23 ปีเมื่อนับชิป
เรือธงทั้ง 43 รุ่นถึงปี 2026 ส่วนที่ Moore พยากรณ์ไว้ในปี 1975 สำหรับจำนวนทรานซิสเตอร์คือสองปี

→ บนสาย K20X → H100 ของ NVIDIA ตัวเลข 501 เท่าแยกได้เป็น ความหนาแน่นทรานซิสเตอร์ 33%, พื้นที่ die 6%,
สัญญาณนาฬิกา 16%, specialization 34% และ precision 11% ของกำไรในสเกล log กฎของ Moore ในความหมายของ
ความหนาแน่นคือราวหนึ่งในสามของกฎของ Huang พจน์เดี่ยวที่ใหญ่ที่สุดคือ matrix unit

→ บัญชีของ NVIDIA เอง (Dally, Hot Chips 2023) ให้เครดิต process 2.5 เท่า และสถาปัตยกรรม 200 เท่า ผลรวมเท่ากัน
แต่ลงบัญชีคนละแบบ: ทรานซิสเตอร์ × สัญญาณนาฬิกา โต 30.5 เท่า หรือ 12 เท่าของตัวคูณ process ของ NVIDIA เพราะ
NVIDIA นับทรานซิสเตอร์ส่วนเกินที่ node ใหม่ให้มาว่าเป็นสถาปัตยกรรม กำไร "มาจากไหน" จึงขึ้นกับว่าใครได้เครดิต
ทรานซิสเตอร์

→ กำแพงหน่วยความจำมีจริงและกว้างขึ้น: แบนด์วิดท์หน่วยความจำเพิ่มสองเท่าทุก 2.70 ปี เทียบกับ 1.23 ปีของการคำนวณ
ดังนั้น operation ต่อไบต์ที่ชิปดึงมาได้เพิ่มสองเท่าทุก 2.20 ปี

→ peak ไม่ใช่งานที่ได้จริง: ใน MLPerf ทั้ง 4 benchmark ที่ตามข้ามรุ่นของ NVIDIA ได้ throughput ต่อตัวเร่งที่วัดจริง
โตช้ากว่าค่า peak ทุกรายการ (ResNet-50 training: 0.45 เทียบกับ 0.85 doubling ต่อปี)

→ การเปิดเผยข้อมูลจบลงในปี 2022 ตั้งแต่ H100 เป็นต้นมา ไม่มีผู้ผลิตรายใดในกลุ่มตัวอย่างเผยทั้งพื้นที่ die และ
สัญญาณนาฬิกาของชิปเรือธง จากเอกสารสาธารณะ การแยกแบบนี้ทำกับ Blackwell, Rubin, MI355X หรือ TPU ไม่ได้

ข้อควรระวังสองข้อที่ควรติดไว้กับทุกกราฟ:
1. ทุกอัตราคือค่า peak ที่ผู้ผลิตประกาศ แบบ dense ไม่รวม sparsity กฎของ Huang พูดถึง peak แต่ peak ไม่ใช่สิ่งที่งาน
training ได้รับ
2. กลุ่มตัวอย่างที่แยกได้ครบมี 9 รุ่น เป็นของ NVIDIA 6 รุ่น เมื่อถดถอยข้ามผู้ผลิต แยกพจน์สถาปัตยกรรมออกจาก
ความหนาแน่นไม่ได้ สมมติฐานที่ลงทะเบียนไว้ข้อนั้นถูกหักล้าง

จากสมมติฐานที่ลงทะเบียนล่วงหน้า 7 ข้อ: สนับสนุน 5 ไม่สนับสนุน 1 หักล้าง 1 ข้อที่ไม่ผ่านอยู่ใน paper ด้วยน้ำหนัก
เท่ากับข้อที่ผ่าน

ทุกอย่างเปิดเผย: ชุดข้อมูลพร้อมที่มาระดับรายค่า (CC BY 4.0) โค้ด (MIT) การลงทะเบียนล่วงหน้าที่แช่แข็งใน git
ก่อนเก็บค่าใด ๆ บันทึกความเบี่ยงเบน และ paper คำสั่งเดียวสร้างทุกตัวเลข ทุกรูป และ PDF ขึ้นใหม่จากข้อมูลที่
commit ไว้ โดยไม่ต้องต่อเน็ต

Independent personal research. Public data only. Does not represent the views of any employer or institution.

#AI #Semiconductors #MooresLaw #GPU #HardwareEngineering #OpenData #Research

คอมเมนต์แรก:
📄 Paper: https://thanatchon36.github.io/chipledger/paper/
💻 Code and data: https://github.com/thanatchon36/chipledger
🤗 Dataset: https://huggingface.co/datasets/thanatchon36/chipledger
🔗 DOI: https://doi.org/10.5281/zenodo.23763729

---

## Variant A: the bookkeeping

Who gets credit for a transistor?

NVIDIA says its flagship inference peak grew 1,000× in a decade, and that process (the chip fab) gave 2.5× of
it. I split the same K20X → H100 gain with an accounting identity, true by construction: density × die area ×
clock × operations per transistor per cycle × narrower number formats.

Same total: 501× dense. But transistors × clock grew 30.5×, twelve times NVIDIA's process factor. The
difference is bookkeeping: NVIDIA counts the extra transistors a new node gives as architecture; the identity
counts them as physics. Neither is wrong. They answer different questions.

On the identity's terms, transistor density, Moore's law in its scaling sense, is 33% of the gain. Matrix units
are 34%. Narrower formats 11%. Clock 16%. Bigger dies 6%.

Pre-registered; 79 accelerators, 14 vendors, 1,152 sourced values; every number in the paper is generated
from the data.

Independent personal research. Public data only. Does not represent the views of any employer or institution.

paper + code + data public, links in the first comment

---

## Variant B: the method

Can you check Huang's law from public documents? Mostly, until 2022.

What I did:
• Pre-registered the question, the identity, the hypotheses and the product list before collecting a value
• Collected 1,152 values for 79 data-centre AI accelerators from 14 vendors, each with a source URL, an access
  date and a confidence level; the vendor's document wins every conflict
• Split every published peak into density × die area × clock × specialization × precision, an identity with no
  residual
• Ran a chip bootstrap for every trend and a sensitivity analysis for every definition

Result: the flagship headline peak doubled every 0.83 years, 2012–2022; density supplied about a third of
NVIDIA's K20X → H100 gain; NVIDIA's own account agrees on the total and differs on who gets the transistors.
Of 7 hypotheses, 5 held, 1 did not, 1 was falsified; the failures are published.

And a finding about the method itself: since H100, no vendor in the sample publishes both die area and clock
for its flagship. The decomposition ends where disclosure ended.

Independent personal research. Public data only. Does not represent the views of any employer or institution.

paper + code + data public, links in the first comment

---

## Variant C: short

AI accelerators' headline peak doubled every 1.23 years, 2012–2026; every 0.83 years on the flagships that
publish every field. Moore's law was two years.

On NVIDIA's K20X → H100 (501×): transistor density 33%, matrix units 34%, narrower formats 11%, clock 16%,
die area 6%. Moore's law is a third of Huang's law.

Vendor peaks, not measured throughput; pre-registered; 79 chips, 14 vendors, 1,152 sourced values.

Independent personal research. Public data only. Does not represent the views of any employer or institution.

paper + code + data public, links in the first comment
