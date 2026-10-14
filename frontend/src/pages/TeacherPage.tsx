import { useParams } from "react-router-dom";


const TeacherPage = () => {

    const {teacherId} = useParams<{ teacherId: string }>();

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold">
                Teacher ID: {teacherId}
            </h1>
            </div>
    );


};

export default TeacherPage;