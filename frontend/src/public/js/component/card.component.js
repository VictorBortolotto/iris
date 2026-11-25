const card = (response) => {
  return `      
    <li class="history-item">
      <div class="history-title">
        <div class="specie">${response.specie}</div>
        <div class="query-date">${response.query_date.split(" ")[0]}</div>
      </div>
      <div class="history-content">
        <div class="line">
          <div class="specie-type" id="iris-setosa">Iris Setosa</div>
          <div class="specie-probabilitie" id="iris-setosa-probabilitie">${response.iris_setosa}</div>
        </div>
        <div class="line">
          <div class="specie-type" id="iris-versicolor">Iris Versicolor</div>
          <div class="specie-probabilitie" id="iris-versicolor-probabilitie">${response.iris_versicolor}</div>
        </div>
        <div class="line">
          <div class="specie-type" id="iris-virginica">Iris Virginica</div>
          <div class="specie-probabilitie" id="iris-virginica-probabilitie">${response.iris_virginica}</div>
        </div>

        <div class="line">
          <div class="specie-type" id="petal-length">Petal Length</div>
          <div class="specie-probabilitie" id="petal-length-probabilitie">${response.petal_length}</div>
        </div>
        <div class="line">
          <div class="specie-type" id="petal-width">Petal Width</div>
          <div class="specie-probabilitie" id="iris-width-probabilitie">${response.petal_width}</div>
        </div>
        <div class="line">
          <div class="specie-type" id="sepal-length">Sepal Length</div>
          <div class="specie-probabilitie" id="sepal-length-probabilitie">${response.sepal_length}</div>
        </div>
        <div class="line">
          <div class="specie-type" id="sepal-width">Sepal Width</div>
          <div class="specie-probabilitie" id="sepal-width-probabilitie">${response.sepal_width}</div>
        </div>

      </div>
    </li>
  `
}