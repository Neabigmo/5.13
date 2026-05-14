# Internal Review (Codex)

Date: 2026-05-14

## Current paper-level claims

1. Uniform replace-one perturbations admit a delete-plus-add upper bound at the
   loss level.
2. Deterministic k-NN prediction changes are exactly margin-crossing events for
   the signed vote over the ordered top-k neighborhood.
3. Deterministic 1-NN admits an explicit finite metric witness where fixed-sample
   LOO stability is zero while replace-one instability is one.
4. Minimality beyond the explicit witness is supported by computational
   certificates only.
5. Odd-k extensions are computational evidence and conjectural lifting, not
   theorem statements.

## Review notes

- The paper now cleanly separates theorem-level claims from certificate-level
  and conjectural claims.
- The main remaining mathematical gap is the absence of a formal odd-k lifting
  proof.
- The current 1-NN witness proof is short enough to hand-check and should remain
  in the main text.
- The reproducibility appendix should continue to be kept in sync with the
  outputs hashes whenever experiments are rerun.

## Residual risk

- The manuscript is now a full draft, but some venue-specific polishing remains:
  tighter introduction prose, possible figure placement tuning, and final
  bibliography style choices.
