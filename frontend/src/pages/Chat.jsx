import { useState, useEffect } from "react"

function Chat() {
    const [chatSessions, setChatSessions] = useState([])

    useEffect(() => {
        async function fetchChatSessions() {
            const token = localStorage.getItem("access_token")

            try {
                const response = await fetch(
                    "http://127.0.0.1:8000/chats",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                if (!response.ok) {
                    throw new Error("Failed to load chat sessions")
                }

                const data = await response.json()
                setChatSessions(data)
            } catch (error) {
                console.log(error)
            }
        }

        fetchChatSessions()
    }, [])

    return (
        <div>
            <h1>Fitness Assitant</h1>

            <h2>Your Chats</h2>

            {chatSessions.map((chat) => (
                <div key={chat.id}>
                    <p>{chat.title}</p>
                </div>
            ))}
        </div>
    )
}

export default Chat