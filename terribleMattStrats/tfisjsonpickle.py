import jsonpickle as jp 

class Thing(object):
    def __init__(self, name):
        self.name = name
        self.value = "ball"

    def sayHi(self):
        print("hello this is awesome")
    

obj = Thing("awesome")
obj.sayHi()

frozen = jp.encode(obj)

thawed = jp.decode(frozen)

print(obj.name== thawed.name)

oneway = jp.encode(obj, unpicklable=False)
result = jp.decode(oneway)
print(obj.name == 'Awesome')


result = {}
orders = [1,2,3,4,5]
product = ["amethyst", "emralds"]

for p in product:
    result[p] = orders

print(result)


print(frozen)
print(thawed)

# We can say this because value and name are a part of the object that we pickled. We can get the values from the constructor this way.
print(thawed.value)
print(thawed.name)
print(thawed.sayHi())

# same thing as doing this basically
print(obj.value)
print(obj.name)
obj.sayHi()

# nice!
print(type(thawed))
print(type(obj))


print(list(result.items())[0])
print(list(result.items())[0][0])
print(list(result.items())[0][1])



