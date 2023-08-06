#include <bits/stdc++.h>

using namespace std;
typedef uint32_t uint;
uint (*funcs[5])(uint);
int *prv;
uint8_t *step;
// uint sponsor1(uint x){
//     return x;
// }
uint sponsor2(uint x) { return x * 3300863383 % 3398445031; }
#define ROR(x, shift) (((x) << (32 - (shift))) | ((x) >> (shift)))
uint power(uint x, uint y) {
  uint ans = 1u;
  while (y) {
    if (y & 1u)
      ans *= x;
    x *= x;
    y >>= 1;
  }
  return ans;
}
uint sponsor3(uint x) { return x * x; }
uint wild2(uint x) { return x + 1; }
uint wild3(uint x) {
  uint r = x & 0x1f;
  uint mask = (1u << r) - 1;
  uint low = (x & mask) << (32 - r);
  uint high = (x ^ low) >> r;
  return (low | high);
}
uint wild4(uint x) {
  uint r = 16;
  uint mask = (1u << r) - 1;
  uint low = (x & mask) << (32 - r);
  uint high = (x ^ low) >> r;
  return (low | high);
}
void bt(uint x) {
  vector<uint> btv;
  vector<int> fstk;
  printf("step:%d\n", step[x]);
  btv.push_back(x);
  for (int ii = 1; ii < step[x]; ii++) {
    for (int i = 0; i < 5; i++) {
      if ((funcs[i])(prv[x]) == x) {
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
  funcs[0] = sponsor2;
  funcs[1] = sponsor3;
  funcs[2] = wild2;
  funcs[3] = wild3;
  funcs[4] = wild4;
  // funcs[5] = sponsor1;
  prv = (int *)malloc(0x100000000llu * sizeof(int));
  step = (uint8_t *)malloc(0x100000000llu * sizeof(uint8_t));
  memset(step, 0, 0x100000000llu * sizeof(uint8_t));
  queue<uint> q;
  q.push(0u);
  step[0] = 1u;
  uint8_t nstep = 2, sz, nxt;
  uint f;
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
      for (int i = 0; i < 5; i++) {
        nxt = (funcs[i])(f);
        // printf("%u ==f(%d)==> %u\n", f, i, nxt);
        fflush(stdout);
        if (step[nxt] != 0)
          continue;
        step[nxt] = nstep;
        prv[nxt] = f;
        q.push(nxt);
      }
    }
    nstep++;
  }

  return 0;
}
