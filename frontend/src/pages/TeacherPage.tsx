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

        })
        .catch((error) => {
            console.error(error);
        });
        }, [teacherId]);

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
            </div>
    );
};

export default TeacherPage;