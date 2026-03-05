**Summary of "Radiation Effects in FPGAs"**  
*J. J. Wang, Actel Corporation*  

---

### **1. Overview**  
The paper addresses radiation-induced performance degradation in FPGAs—specifically Total Ionizing Dose (TID) and Single Event Effects (SEE)—for space applications. Radiation hardiness is critical for aerospace systems due to high radiation environments. Antifuse-based FPGAs dominate due to their radiation tolerance, while SRAM-based FPGAs suffer from config bit SEUs, and flash FPGAs require further study. The paper correlates observed anomalies (e.g., power supply current spikes, propagation delays) with radiation mechanisms (charge trapping, SEU propagation) and discusses hardening strategies.  

---

### **2. Methods**  
Testing followed military standard TM1019 for TID, using static bias and gamma irradiation (Co-60 source). SEE testing involved shift-registerbased DUTs with error counting for SEUs. Key parameters measured: power supply current (\(I_{CC}\)), propagation delay (\(T_p\)), and error rates. Characterization included pre/post-irradiation analysis and annealing effects.  

---

### **3. Results & Data**  
- **TID Effects**:  
  - **Antifuse**: Immune to TID; failures occurred in charge pump circuits (e.g., ICC jumps at ~30 krad).  
  - **SRAM**: Configuration bit SEUs caused functional failures after ~50 krad.  
  - **Flash**: Floating gate degradation led to propagation delay issues, but data is preliminary.  
- **SEE Effects**:  
  - **Antifuse**: SEUs in buffers/clock networks caused clock upsets and control logic errors. Hardening via TMR latches reduced SEU susceptibility.  
  - **Flash**: SELs mitigated in newer ProASIC-PLS via epi-substrate; no SEU observed on flash switches.  
- **Key Data**:  
  - Tables 1 & 2 show error rates and cross-sections for SRAM switches at varying altitudes.  
  - Figures (e.g., 5, 8) depict ICC and \(T_p\) degradation.  

---

### **4. Limitations & Future Work**  
- **SRAM-based FPGAs**: Configuration bit SEUs complicate analysis; hardware hardening is costly.  
- **Flash-based FPGAs**: Limited radiation data due to recent adoption.  
- **Future Work**: Improved flash device radiation models, dynamic SEU testing, and SEU mechanisms in complex architectures.  

---

### **5. Key Terms**  
- **TID**: Total Ionizing Dose effect from charge trapping in oxides.  
- **SEE**: Single Event Effect, causing temporary storage element errors.  
- **SEU**: Single Event Upset, a type of SEE flipping bits.  
- **CPLD**: Complex Programmable Logic Device (older tech).  
- **LUT**: Look-Up Table in FPGA logic modules.  
- **TMR**: Triple-Module Redundancy for error correction.  

---

### **6. Equations**  
The paper describes radiation mechanisms qualitatively (e.g., charge trapping in Si/SiO₂ interfaces) but does not provide explicit formulas. Key processes include:  
- Hole trapping near dielectrics inducing leakage (Figures 2–3).  
- SEU competition between feedback/recovery processes (Figures 15–16).  

---

**Citations Preserved**:  
- Military standard [7] for TID testing,  
- [15] for SEE methodologies,  
- [17] for SEU mechanisms.  

This summary balances technical depth with clarity for knowledgeable readers, emphasizing FPGA-specific radiation challenges and mitigation strategies.