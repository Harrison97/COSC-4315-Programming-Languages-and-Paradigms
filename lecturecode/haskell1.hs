import Text.Show.Functions

inc n = n + 1

len :: [a] -> Int
len [] = 0
len (x:xs) = 1 + len xs


map' :: [a] -> (a -> b) -> [b]
map' [] f = []
map' (x:xs) f = (f x): map' xs f


fact :: Int -> Int
fact 0 = 1
fact n = n* fact (n - 1)

fact' :: Int -> Int -> Int
fact' 0 res = res
fact' n res = fact' (n-1) (n*res)

data BB = T | F

and' :: BB -> BB -> BB
and' F _ = F
and' T x = x


data BST a = Leaf a | Node a (BST a) (BST a)

data Colors = Red | Yellow | Green
data Action = Stop | Yield | SpeedUp

car Red = Stop
car Yellow = Yield
car Green = SpeedUp

type CarAction = (Colors, Action)

data DriverType = Good | Bad deriving Show

-- Instance Show DriverType where
-- show Good = "Good"
-- show Bad = "Bad"

isValid :: CarAction -> DriverType
isValid (Green, SpeedUp) = Good
isValid (Green, _ ) = Bad

myList = [1, 2, 3, 0, -2]

myList' = [(\x -> x^2) | x <- myList]

