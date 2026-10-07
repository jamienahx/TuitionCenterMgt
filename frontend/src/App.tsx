import {useEffect, useState} from "react";

interface Availability {
  day_of_week: string;
  start_time: string;
  end_time: string;
}

interface Teacher {
  id: number;
  name: string;
  contact_number:string;
  subjects: string[];
  levels: string[];
  availability: Availability[];
}
const App = () => {

  const[teachers, setTeachers] = useState<Teacher[]>([]);
  useEffect(()=> {
    fetch("http://127.0.0.1:8000/api/teachers/")
    .then((response)=> response.json())
    .then((data)=>{
      setTeachers(data);
      console.log(data);
    });
  }, []);

  return (
    <div>
    <h1 className="text-5xl font-bold text-blue-600">Relief Teacher</h1>
<table>
  <thead>
    <tr>
    <th>Name</th>
    <th>Contact Number</th>
    <th>Subjects</th>
    <th>Levels</th>
    <th>Day of Week</th>
    <th>Start Time</th>
    <th>End Time</th>
    </tr>
  </thead>
  <tbody>
    {teachers.map((teacher)=> (
    <tr key ={teacher.id}>
    <td>{teacher.name}</td>
    <td>{teacher.contact_number}</td>
    <td>
      {teacher.subjects.map((subject)=>(
        <p key = {subject}>{subject}/</p>
          )
        )
      }
      </td>
      <td>
      {teacher.levels.map((level)=>(
        <p key = {level}>{level}/</p>
          )
        )
      }
    </td>
    
    <td>
      {teacher.availability.map((slot,index) => (
        <div key = {index}>
         <p>{slot.day_of_week}</p>
         <p>{slot.start_time}</p>
           <p>{slot.end_time}</p>
           </div>
           )
          )
        }
        </td>
    </tr>
      )
    )
  }
  </tbody>
  </table>
</div>

);


};

export default App;