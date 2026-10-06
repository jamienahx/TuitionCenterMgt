import {useEffect, useState} from "react";


const App = () => {

  const[teachers, setTeachers] = useState([]);
  useEffect(()=> {
    fetch("http://127.0.0.1:8000/api/teachers/")
    .then((response)=> response.json())
    .then((data)=>{
      setTeachers(data);
      console.log(data);
    });
  }, []);

  return (
    <h1 className="text-5xl font-bold text-blue-600">Relief Teacher</h1>
  );
};

export default App;