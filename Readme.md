> Question: how you would plan to give an admin the ability to check the balance of a user at a given time 

> Answer: The current transaction model is used as a historical data for each payment process so that it will store the total balance on every row.
> As a result, when you look back to specific date, you will run one query to get transaction happened just before than the given date.
> Ex: Foo: 2023-02-04, Bar: 2023-02-06, if you set filter with 2023-02-05, then it will pick Foo.


> Question: As a bonus, can you write in the README your thoughts about performance and scalability. 
What would be the most efficient way to retrieve the balance 
if there are millions of transactions and/or if there are 1,000 transactions/s?

> The current model is using "-date" default ordering, that's said, you can just get the top one to know the most recent balance.
> The DB query time will be much short to get the first record.
