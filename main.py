from CollectInfo import Collect

stock = input('What stock would you like to check?')
test = Collect(stock)

print(test.get_sentiment())
