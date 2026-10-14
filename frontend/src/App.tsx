import { Routes, Route } from "react-router-dom";
import TeachersPage from "./pages/TeachersPage";
import TeacherPage from "./pages/TeacherPage";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<TeachersPage />} />
      <Route path ="/teachers/:teacherId" element ={<TeacherPage />} />
    </Routes>
  )
}

export default App;