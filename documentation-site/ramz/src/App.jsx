import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, Outlet } from 'react-router-dom';

import LanguageReference from './components/LanguageReference';
import MainPage from './pages/MainPage';
import SyntaxPage from './pages/SyntaxPage';

import './App.css';


function Layout() {
    return (
        <div className="vh-100 overflow-hidden bg-light">

            <div className="container-fluid h-100 p-0">

                <div className="d-flex h-100">

                    {/* Sidebar */}
                    <aside
                        className="bg-white border-end h-100 overflow-auto p-3 flex-shrink-0 sidebar"
                    >
                        <LanguageReference />
                    </aside>


                    {/* Main Content */}
                    <main className="flex-grow-1 h-100 overflow-auto responsive-main-padding">

                        <Outlet />

                    </main>

                </div>

            </div>

        </div>
    );
}


function App() {
    return (
        <Routes>

            <Route element={<Layout />}>

                <Route path="/" element={<MainPage />} />

                <Route path="/main" element={<MainPage />} />

                <Route path="/syntax" element={<SyntaxPage />} />

            </Route>

        </Routes>
    );
}

export default App;