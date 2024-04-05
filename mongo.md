
1. Create Database

```
use db
show dbs
```

2. Create collection
```js
db.movies.insertMany([
  {
    "id": "99",
    "name": "Vikram",
    "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
    "rating": 8.4,
    "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
    "trailer": "https://www.youtube.com/embed/OKBMCL-frPU"
...........
)
```

3. Read the data

```sql
Select * from movies
```

```js
db.movies.find()
```

4. Filter the data

```js
db.collection.find({
  "id": "100"
})
```


## Comparison operators

5. All the movies with rating exactly 8


```js
db.collection.find({
  rating: 8
})
```

All operators will start with `$`


5.1 Negative the above


```js
db.collection.find({
  rating: {
    $ne: 8
  }
})
```



1. All the movies with rating more than 8

```js
db.collection.find({
  rating: {
    $gt: 8
  }
})
```

7. All the movies with rating less than 8

```js
db.collection.find({
  rating: {
    $lt: 8
  }
})
```

8. All the movies with rating less than and including 8


```js
db.collection.find({
  rating: {
    $lte: 8
  }
})
```

9. All the movies with rating more than and including 8

```js
db.collection.find({
  rating: {
    $gte: 8
  }
})
```

10. All the movies which rating 8.4, 7, 8.1
Clue: Same operator in SQL 


```js
db.collection.find({
  rating: {
    "$in": [
      8.4,
      7,
      8.1
    ]
  }
})
```

11. Negative of the above

```js
db.collection.find({
  rating: {
    "$nin": [
      8.4,
      7,
      8.1
    ]
  }
})
```

Task 
1. flash - notification
2. Write equivalent Sql commands
3. Read about hash vs encryption



```js
db.collection.find({
  rating: {
    $gt: 8
  }, {_id:0, name: 1, rating: 1 }
})
```


```js
db.collection.find({}).sort({rating: 1})
```


```js
db.movies.find({},  {_id:0, rating:1, name: 1}).sort({rating: -1})
```

## Compound sorting

Expected output
J
R
T

```js
db.movies.find({},  {_id:0, rating:1, name: 1}).sort({rating: -1, name: 1})
```

## Top 3  - limit

```js
db.movies.find({},  {_id:0, rating:1, name: 1}).sort({rating: -1, name: 1}).limit(3)
```
## Skip 3  - skip


<!-- 4th, 5th, 6th -->


```js
db.movies.find({},  {_id:0, rating:1, name: 1}).sort({rating: -1, name: 1}).limit(3).skip(3)
```



```js
db.orders.insertMany([
{ _id: 0, productName: "Steel beam", status: "new", quantity: 10 },
{ _id: 1, productName: "Steel beam", status: "urgent", quantity: 20 },
{ _id: 2, productName: "Steel beam", status: "urgent", quantity: 30 },
{ _id: 3, productName: "Iron rod", status: "new", quantity: 15 },
{ _id: 4, productName: "Iron rod", status: "urgent", quantity: 50 },
{ _id: 5, productName: "Iron rod", status: "urgent", quantity: 10 }
])
```

Expected Output

```js
[
{ _id: "Steel beam",  totalQuantity: 50 },
{ _id:"Iron rod", totalQuantity: 60 }
]

```


```sql

```

```js
db.orders.aggregate([
  {$match: {status: 'urgent'}}
])

```