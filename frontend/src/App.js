import './App.css';
import {useState, useEffect} from "react";

function App() {

  const[customers, setCustomers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get", {
      "method":"GET",
      headers: {
        "Content-Type":"application/json"
      }
    })
    .then(resp => resp.json())
    .then(resp => console.log(resp))
    .catch(error => console.log(error))
  });

  return (
    <div className="App">
      <h1>Flask</h1>

      {customers.map(customer => {
        return (
          <div key = {customer.id}>
            <h2>{customer.first_name}</h2>
          </div>
        )
      })}
    </div>
  );
}

export default App;
