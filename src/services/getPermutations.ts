export function getPermutations<T>(array: T[]): T[][] {
    function permute(arr: T[], memo: T[] = []): T[][] {
      let cur: T[];
      let permutations: T[][] = [];
  
      for (let i = 0; i < arr.length; i++) {
        cur = arr.splice(i, 1);
        if (arr.length === 0) {
          permutations.push(memo.concat(cur));
        }
        const permuted = permute(arr.slice(), memo.concat(cur));
        permutations = permutations.concat(permuted);
        arr.splice(i, 0, cur[0]);
      }
  
      return permutations;
    }
  
    return permute(array);
  }