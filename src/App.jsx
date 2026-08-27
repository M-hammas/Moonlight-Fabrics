import React from "react";
import {BrowserRouter} from "react-router-dom";
import AppRoutes from "./routes";
import NotificationToast from "./components/common/NotificationToast";
export default function App(){return <BrowserRouter><AppRoutes/><NotificationToast/></BrowserRouter>}
