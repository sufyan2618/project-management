import { createContext, useState, useEffect, useContext, use } from "react";
import { io } from "socket.io-client"
import { useSelector } from "react-redux";

const socketContext = createContext();

export const useSocket = () => useContext(socketContext);

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const { token , isAuthenticated } = useSelector((state) => state.auth);

    useEffect(() => {
        if (isAuthenticated && token) {
            const newSocket = io("http://localhost:8000", {
                query: { token }
            });
            setSocket(newSocket);
            
            newSocket.on("connect", () => {
                console.log("Connected to socket server");
            });

            return () => {
                newSocket.disconnect();
            }
        } else if (!isAuthenticated && socket) {
            socket.disconnect();
            setSocket(null);
        }
    }, [isAuthenticated, token]);

    return (
        <socketContext.Provider value={socket}>
            {children}
        </socketContext.Provider>
    );
};