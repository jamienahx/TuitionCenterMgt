import {useEffect, useState} from "react";
import { useNavigate } from "react-router-dom"



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


  const navigate = useNavigate();
  const[teachers, setTeachers] = useState<Teacher[]>([]);
  const [editingTeacher, setEditingTeacher] = useState <Teacher | null>(null);

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
<table className="w-full border-collapse">
  <thead className="bg-gray-100">
    <tr>
    <th className="border border-gray-300 px-4 py-3 text-left">Name</th>
    <th className="border border-gray-300 px-4 py-3 text-left">Contact Number</th>
    <th className="border border-gray-300 px-4 py-3 text-left">Subjects</th>
    <th className="border border-gray-300 px-4 py-3 text-left">Levels</th>
    <th className="border border-gray-300 px-4 py-3 text-left">Day of Week</th>
    <th className="border border-gray-300 px-4 py-3 text-left">Start Time</th>
    <th className="border border-gray-300 px-4 py-3 text-left">End Time</th>
    <th className = "border border-gray-300 px-4 py-3 text-left">Actions</th>
    </tr>
  </thead>
  
  <tbody>
    {teachers.map((teacher)=> (
    
    <tr key ={teacher.id}
      className="border-b-2">
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
        <div key = {index}>{slot.day_of_week}</div>
          )
        )
      }
      </td>   
      <td>
        {teacher.availability.map((slot,index) => (
        <div key = {index}>{slot.start_time}</div>
          )
        )
      }
      </td>
      <td>
        {teacher.availability.map((slot,index) => (
        <div key = {index}>{slot.end_time}</div>
          )
        )
      }
      </td>
      <td className="border border-gray-300 px-4 py-3">
      <button
        type="button"
        onClick={()=> navigate (`/teachers/${teacher.id}`)}
        className="rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700">Edit</button>
        </td>
          
    </tr>
      )
    )
  }
  </tbody>
  </table>

  {editingTeacher && (
    <div className="mt-6">
      <h2 className="text-2xl font-bold">
        Editing: {editingTeacher.name}
      </h2>
      </div>
  )}
</div>

);


};

export default App;