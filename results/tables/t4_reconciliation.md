# Estimator (c): K20X → H100 SXM against NVIDIA's account

| factor | identity A (primary reference) | identity A (FP32 reference) | NVIDIA (Dally 2023) |
|---|---|---|---|
| headline rate | 3.95 fp32 → 1979.0 fp8_tensor |  |  |
| total (dense) | 501.0× | 501.0× | 500× (1000× with 2× sparsity) |
| density | 7.63× | 7.63× |  |
| area | 1.48× | 1.48× |  |
| clock | 2.70× | 2.70× |  |
| **physical: N·f** | **30.5×** | 30.5× | process 2.5× |
| specialization | 8.22× | 0.56× | complex instructions 12.5× |
| precision multiplier | 2.00× | 29.54× | number representation 16.0× |
| **non-physical: spec × precision** | **16.4×** | 16.4× | 200× |
