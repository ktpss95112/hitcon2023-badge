#include <bits/stdc++.h>
#define FUNC_N 21
using namespace std;
typedef uint32_t uint;

uint (*funcs[FUNC_N])(uint);
uint *prv;
uint16_t *step;
uint sponsor01(uint x) {
  static char str[] = "DVCR";
  return x ^ *(int *)str;
}
uint sponsor02(uint x) {
  static char str[] = "CRFT";
  return x ^ *(int *)str;
}
uint sponsor03(uint x) {
  static char str[] = "2317";
  return x ^ *(int *)str;
}
uint sponsor04(uint x) {
  static char str[] = "ISIP";
  return x ^ *(int *)str;
}
uint sponsor05(uint x) {
  static char str[] = "KKCO";
  return x ^ *(int *)str;
}
uint sponsor06(uint x) {
  static char str[] = "CHTS";
  return x ^ *(int *)str;
}
uint sponsor07(uint x) {
  static char str[] = "TRPA";
  return x ^ *(int *)str;
}
uint sponsor08(uint x) {
  static char str[] = "RKTN";
  return x ^ *(int *)str;
}
uint sponsor09(uint x) {
  static char str[] = "KBOX";
  return x ^ *(int *)str;
}
uint sponsor10(uint x) {
  static char str[] = "OFSC";
  return x ^ *(int *)str;
}
uint wild01(uint x) { return 0u; }
uint wild02(uint x) { return x + 1u; }
uint wild03(uint x) { return x + 2u; }
uint wild04(uint x) { return x + 3u; }
uint wild05(uint x) { return x + 4u; }
uint wild06(uint x) { return x + 5u; }
uint wild07(uint x) { return x + 6u; }
uint wild08(uint x) { return x + 7u; }
uint wild09(uint x) { return x + 8u; }
uint wild10(uint x) { return x + 9u; }
uint wild11(uint x) {
  uint r = x & 0x1fu;
  return (x << (32 - r)) | (x >> r);
}
uint wild12(uint x) { return (x << 16) | (x >> 16); }

void bt(uint x) {
  vector<uint> btv;
  vector<uint> fstk;
  btv.push_back(x);
  uint nxt, stp = step[x];
  printf("step:%u\n", stp);
  for (int ii = 1; ii < stp; ii++) {
    for (int i = 0; i < FUNC_N; i++) {
      nxt = funcs[i](prv[x]);
      if (nxt == x) {
        btv.push_back(prv[x]);
        fstk.push_back(i);
        break;
      }
    }
    x = prv[x];
  }
  printf("%u", btv[0]);
  for (int i = 1; i < btv.size(); i++) {
    printf("<==f(%d)==%u", fstk[i - 1], btv[i]);
  }
  puts("");
  fflush(stdout);
}

int main() {
  funcs[0] = sponsor01;
  funcs[1] = sponsor02;
  funcs[2] = sponsor03;
  funcs[3] = sponsor04;
  funcs[4] = sponsor05;
  funcs[5] = sponsor06;
  funcs[6] = sponsor07;
  funcs[7] = sponsor08;
  funcs[8] = sponsor09;
  funcs[9] = sponsor10;
  // funcs[10] = wild01;
  funcs[10] = wild02;
  funcs[11] = wild03;
  funcs[12] = wild04;
  funcs[13] = wild05;
  funcs[14] = wild06;
  funcs[15] = wild07;
  funcs[16] = wild08;
  funcs[17] = wild09;
  funcs[18] = wild10;
  funcs[19] = wild11;
  funcs[20] = wild12;
  prv = (uint *)malloc(0x100000000llu * sizeof(uint));
  step = (uint16_t *)malloc(0x100000000llu * sizeof(uint16_t));
  memset(step, 0, 0x100000000llu * sizeof(uint16_t));
  queue<uint> q;
  q.push(0u);
  step[0] = 1u;
  uint16_t nstep = 2;
  uint f, nxt, sz;
  prv[0] = 0;
  int all = 32 * 31 / 2;
  while (!q.empty() && all) {
    sz = q.size();
    for (int i = 0; i < sz; i++) {
      f = q.front();
      q.pop();
      if (__builtin_popcount(f) == 2) {
        bt(f);
        all--;
      }
      for (int j = 0; j < FUNC_N; j++) {
        nxt = funcs[j](f);
        // printf("f[%d](%u) = %u\n", j, f, nxt);
        // fflush(stdout);
        if (step[nxt] != 0u)
          continue;
        step[nxt] = nstep;
        prv[nxt] = f;
        q.push(nxt);
      }
    }
    nstep++;
    if (nstep >= 12)
      break;
  }
  if (q.empty())
    puts("q empty");
  else
    puts("all = 0");

  return 0;
}
// 1056 <= = (+2) == 1054 <= = wild04 == 69074944 <= = wild3 == 527 <=
//     = sponsor01 == 1380144203 <= = (+5) == 1380144198 <=
//     = wild04 == 1413894723 <= = sponsor02 == 0
