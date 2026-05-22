import ChatPage from "./pages/chat-page";
import Dashboard from "./pages/dashboard";

import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<ChatPage />} />
                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;