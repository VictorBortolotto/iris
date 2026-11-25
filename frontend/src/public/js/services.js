const DEFAULT_URL = "http://localhost:8080/prediction"

const predict = async (data) => {
  const response = await fetch(DEFAULT_URL + `/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
    mode: 'cors'
  });

  return response;
};

const get_stats = async () => {
  const response = await fetch(DEFAULT_URL + `/stats`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    mode: 'cors' 
  });

  return response
}

const get_all_predctions = async (param = '') => {

  const response = await fetch(DEFAULT_URL + `/all?specie=${param}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    mode: 'cors' 
  });

  return response
}

const get_predction_by_id = async (id) => {

  const response = await fetch(DEFAULT_URL + `/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    mode: 'cors' 
  });

  return response
}