import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

interface Availability {
    day_of_week: string;
    start_time:string;
    end_time: string;
}

interface Teacher {
    id: number;
    name: string;
    contact_number: string;
    subjects: string[];
    levels: string[];
    availability: Availability[];
}


const TeacherPage = () => {

    const { teacherId } = useParams<{ teacherId: string }>();

    //during the initial render the interface may be null bc it hasnt connected to the BE yet. Once the teacher object is retrieved it will render the teacher object with its attributes defined in the interface
    const [teacher, setTeacher] = useState<Teacher | null>(null);
    const [subjectsInput, setSubjectsInput] = useState("");
    const [levelsInput, setLevelsInput] = useState("");
     
    useEffect (() => {
        fetch("http://127.0.0.1:8000/api/teachers/")
        .then((response) =>{
            if(!response.ok) {
                throw new Error("Failed to fetch teachers");
            }
            return response.json();
        })
        .then((data: Teacher[])=> {
            const selectedTeacher = data.find(
                (item) => item.id=== Number(teacherId)         );

        setTeacher(selectedTeacher ?? null);
        setSubjectsInput(selectedTeacher?.subjects.join(", ") ?? "")
        setLevelsInput(selectedTeacher?.levels.join(", ") ?? "")

        })
        .catch((error) => {
            console.error(error);
        });
        }, [teacherId]);

        const handleSave = async () => {

            if(!teacher) return;

            const updatedTeacher = {
                ...teacher,
                subjects: subjectsInput.split(",").map((subject)=> subject.trim()).filter(Boolean),
                levels: levelsInput.split(",").map((level) => level.trim()).filter(Boolean)
            }
        

        const response = await fetch (
            `http://127.0.0.1:8000/api/teachers/${teacher.id}/`,
            {
                method:"PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(updatedTeacher)
            }
        );
        

        if(!response.ok){

            console.error("Failed to save")
            return;

        }

        const savedTeacher: Teacher = await response.json();
        setTeacher(savedTeacher);
        console.log("Teacher details updated");
        };

        if(!teacher) {
            return <p className="p-6">Loading teacher or teacher not found</p>

        }
    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">
                Edit Teacher
            </h1>
            <div className="mb-4">
                <label className="block font-medium mb-2">Name</label>
            <input type="text"
                    value={teacher.name}
                    onChange={(e)=>
                        setTeacher({...teacher, name: e.target.value})
            }
            className="w-full border border-gray-300 rounded px-3 py-2"/>
            </div>

            <div className="mb-4">
                <label className="block font-medium mb-2">Contact Number</label>
            <input type="text"
                    value={teacher.contact_number}
                    onChange={(e)=>
                        setTeacher({...teacher, contact_number: e.target.value})
            }
            className="w-full border border-gray-300 rounded px-3 py-2"/>
            </div>

            <div className="mb-4">
                <label className="block font-medium mb-2">Subjects</label>
            <input type="text"
                    value={subjectsInput}
                    onChange={(e)=> setSubjectsInput(e.target.value)}
                       
            
            className="w-full border border-gray-300 rounded px-3 py-2"/>
            </div>

            <div className="mb-4">
                <label className="block font-medium mb-2">Levels</label>
            <input type="text"
                    value= {levelsInput}
                    onChange={(e)=>
                        setLevelsInput(e.target.value)
            }
            className="w-full border border-gray-300 rounded px-3 py-2"/>
            </div>

            <div className="mb-4">
                <label className="block font-medium mb-2">Availability (Day, Start Time, End Time)</label>
                {teacher.availability.map((slot, index)=> (
                    <div key={index} className="mb-4">
                        <input
                            type="text"
                            value={slot.day_of_week}
                            onChange={(e) => {
                                const updatedAvailability = [...teacher.availability];

                                updatedAvailability[index] = {
                                    ...slot,
                                    day_of_week: e.target.value
                                };

                                setTeacher({
                                    ...teacher,
                                    availability: updatedAvailability
                                });
                            }}

                            className="w-full border border-gray-300 rounded px-3 py-2 mb-2"/>
                            
                        
                            <input
                            type="time"
                            value={slot.start_time}
                            onChange={(e) => {
                                const updatedAvailability = [...teacher.availability];

                                updatedAvailability[index] = {
                                    ...slot,
                                    start_time: e.target.value
                                };

                                setTeacher({
                                    ...teacher,
                                    availability: updatedAvailability
                                });
                            }}

                            className="w-full border border-gray-300 rounded px-3 py-2 mb-2"/>

                            <input
                            type="time"
                            value={slot.end_time}
                            onChange={(e) => {
                                const updatedAvailability = [...teacher.availability];

                                updatedAvailability[index] = {
                                    ...slot,
                                    end_time: e.target.value
                                };

                                setTeacher({
                                    ...teacher,
                                    availability: updatedAvailability
                                });
                            }}

                            className="w-full border border-gray-300 rounded px-3 py-2 mb-2"/>
               </div>
             ))}
            </div>
            <button 

             onClick={handleSave}
                type="button"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                    Save Changes
                </button>
    </div>
    );
};

export default TeacherPage;