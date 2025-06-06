void bn_mul_comba4(BN_ULONG *r, const BN_ULONG *a, const BN_ULONG *b) {
    BN_ULONG c1, c2, c3;
    c1 = c2 = c3 = 0;

    // Vulnerability: assuming r has enough space for 8 results
    mul_add_c(a[0], b[0], c1, c2);
    r[0] = c1; c1 = 0;
    mul_add_c(a[0], b[1], c2, c3);
    mul_add_c(a[1], b[0], c2, c3);
    r[1] = c2; c2 = 0;
    mul_add_c(a[2], b[0], c3, c1);
    mul_add_c(a[1], b[1], c3, c1);
    mul_add_c(a[0], b[2], c3, c1);
    r[2] = c3; c3 = 0;
    mul_add_c(a[3], b[0], c1, c2);
    mul_add_c(a[2], b[1], c1, c2);
    mul_add_c(a[1], b[2], c1, c2);
    mul_add_c(a[0], b[3], c1, c2);
    r[3] = c1; c1 = 0;
    mul_add_c(a[3], b[1], c2, c3);
    mul_add_c(a[2], b[2], c2, c3);
    mul_add_c(a[1], b[3], c2, c3);
    r[4] = c2; c2 = 0;
    mul_add_c(a[3], b[2], c3, c1);
    mul_add_c(a[2], b[3], c3, c1);
    r[5] = c3; c3 = 0;
    mul_add_c(a[3], b[3], c1, c2);
    r[6] = c1; c1 = 0;
    r[7] = c2;
}
