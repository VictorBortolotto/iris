create table if not exists request_data(
  id integer primary key,
  sepal_length float not null,
  sepal_width float not null,
  petal_length float not null,
  petal_width float not null
);

create table if not exists query_data(
  id integer primary key,
  specie varchar(200) not null,
  iris_setosa float not null,
  iris_versicolor float not null,
  iris_virginica float not null,
  query_date datetime null,
  id_request_data integer references request_data(id)
);