-- Move from A to B with C as temperory
type Peg = String
type Move = (Peg, Peg)

hanoi :: Integer -> Peg -> Peg -> Peg -> [Move]
hanoi n s d t
  | n <= 0 = []
  | n == 1 = [(s, d)]
  | otherwise = hanoi (n - 1) s t d ++ hanoi 1 s d t ++ hanoi (n - 1) t d s

-- Quick Sort

-- quickSort(arr[], low, high)
-- {
--     if (low < high)
--     {
--         pi = partition(arr, low, high);
--         quickSort(arr, low, pi - 1);  // Before pi
--         quickSort(arr, pi + 1, high); // After pi
--     }
-- }
-- partition (arr[], low, high)
-- {
--     pivot = arr[high];
--     i = (low - 1)  // Index of smaller element
--     for (j = low; j <= high- 1; j++)
--     {
--         if (arr[j] < pivot)
--         {
--             i++;    // increment index of smaller element
--             swap arr[i] and arr[j]
--         }
--     }
--     swap arr[i + 1] and arr[high])
--     return (i + 1)
-- }

qsort :: [Int] -> [Int]
qsort [] = []
qsort (x:xs) = qsort (filter (< x) xs) ++ [x] ++ qsort (filter (>= x) xs)

-- Fibonacci
fib :: Int -> Int
fib n
  | n <= 0 = 1
  | n == 1 = 1
  | otherwise = fib(n - 1) + fib(n - 2)

-- repli "abc" 3
-- "aaabbbccc"

repli :: [a] -> Int -> [a]
repli xs n = concatMap (replicate n) xs

repli' :: [a] -> Int -> [a]
repli' xs n = xs >>= replicate n
