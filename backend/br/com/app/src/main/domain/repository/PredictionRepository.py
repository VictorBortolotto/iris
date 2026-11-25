from database.Database import Database
from domain.dto.ConsultPredictionDto import ConsultPredictionDto
from domain.dto.PredictionStatsDto import PredictionStatsDto

class PredictionRepository:
  def __init__(self):
    self.database = Database()

  def insert_request_data(self, request):
    result = self.database.insert("insert into request_data (sepal_length,sepal_width,petal_length,petal_width) values (?,?,?,?)", (
      request["sepal_length"],
      request["sepal_width"],
      request["petal_length"],
      request["petal_width"]
    ))

    return result

  def insert_query_data(self, specie, iris_setosa, iris_versicolor, iris_virginica, query_date, id_request_data):
    result = self.database.insert("insert into query_data (specie,iris_setosa,iris_versicolor,iris_virginica,query_date,id_request_data) values (?,?,?,?,?,?)", (
      specie,
      iris_setosa,
      iris_versicolor,
      iris_virginica,
      query_date,
      id_request_data
    ))

    return result

  def find_all_prediction(self, nm_specie):
    results = self.database.find_all_by("select qd.id, sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date from request_data rd, query_data qd where rd.id = qd.id_request_data and (? is null or qd.specie = ?)", (nm_specie,nm_specie))

    if results is None:
      return results
    
    consult_list = []
    for result in results:
      id,sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date = result
      consult_list.append(ConsultPredictionDto(id,sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date))

    return consult_list

  def find_prediction_by_id(self, id):
    result = self.database.find_by_id("select qd.id, sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date from request_data rd, query_data qd where qd.id = ? and rd.id = qd.id_request_data", (id,))

    if result is None:
      return result

    id,sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date = result

    return ConsultPredictionDto(id,sepal_length,sepal_width,petal_length,petal_width,specie,iris_setosa,iris_versicolor,iris_virginica,query_date)
  
  def prediction_stats(self):
    result = self.database.find_by_id("""
      SELECT
          COUNT(*) AS total_classifications,

          SUM(CASE
              WHEN specie = 'Iris Setosa' THEN 1
              ELSE 0
          END) AS setosa_count,

          ROUND(
              SUM(CASE WHEN specie = 'Iris Setosa' THEN 1 ELSE 0 END)
              * 100.0 / NULLIF(COUNT(*), 0), 2
          ) AS setosa_percentage,

          SUM(CASE
              WHEN specie = 'Iris Versicolor' THEN 1
              ELSE 0
          END) AS versicolor_count,

          ROUND(
              SUM(CASE WHEN specie = 'Iris Versicolor' THEN 1 ELSE 0 END)
              * 100.0 / NULLIF(COUNT(*), 0), 2
          ) AS versicolor_percentage,

          SUM(CASE
              WHEN specie = 'Iris Virginica' THEN 1
              ELSE 0
          END) AS virginica_count,

          ROUND(
              SUM(CASE WHEN specie = 'Iris Virginica' THEN 1 ELSE 0 END)
              * 100.0 / NULLIF(COUNT(*), 0), 2
          ) AS virginica_percentage
        FROM query_data qd;
    """, ())

    if result is None:
      return result

    total_classifications,setosa_count,setosa_percentage,versicolor_count,versicolor_percentage,virginica_count,virginica_percentage = result

    return PredictionStatsDto(total_classifications,setosa_count,setosa_percentage,versicolor_count,versicolor_percentage,virginica_count,virginica_percentage)