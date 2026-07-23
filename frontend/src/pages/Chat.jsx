import { useState, useEffect } from "react"

function Chat() {
    const [chatSessions, setChatSessions] = useState([])
    const [selectedChat, setSelectedChat] = useState(null)
    const [messageInput, setMessageInput] = useState("")
    const [isLoading, setIsLoading] = useState(false)

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

    async function selectChat(sessionId) {
        const token = localStorage.getItem("access_token")

        try {
            const response = await fetch(
                `http://127.0.0.1:8000/chats/${sessionId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    }
                }
            )

            if (!response.ok) {
                throw new Error("failed to load chat")
            }

            const data = await response.json()

            setSelectedChat(data)
        } catch (error){
            console.log(error)
        }
    }

    async function createNewChat() {
        const token = localStorage.getItem("access_token")

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/chats",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        title: "New Conversation",
                    }),
                }
            )

            if (!response.ok){
                throw new Error("Failed to create chat")
            }

            const newChat = await response.json()

            setChatSessions((currentChat) => [
                ...currentChat,
                newChat,
            ])

            setSelectedChat({
                ...newChat,
                messages: [],
            })
        }catch (error){
            console.log(error)
        }
    }

    async function sendMessage(event) {
        event.preventDefault()

        if (!selectedChat || !messageInput.trim()) {
            return
        }

        const token = localStorage.getItem("access_token")

        setIsLoading(true)

        try {
            const response = await fetch(
                `http://127.0.0.1:8000/chats/${selectedChat.id}/messages`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        content: messageInput,
                    }),
                }
            )

            if (!response.ok){
                throw new Error("failed to send message")
            }

            const data = await response.json()

            setSelectedChat((currentChat) => ({
                ...currentChat,
                messages: [
                    ...currentChat.messages,
                    data.user_message,
                    data.assistant_message,
                ],
            }))

            setMessageInput("")
        }catch(error){
            console.log(error)
        } finally{
            setIsLoading(false)
        }
    }

    function logout() {
        localStorage.removeItem("access_token")
        window.location.href = "/"
    }

    return (
        <div>
            <h1>Fitness Assitant</h1>

            <button onClick={logout}>
                Logout
            </button>

            <button onClick={createNewChat}>
                New Chat
            </button>

            <h2>Your Chats</h2>

            {chatSessions.map((chat) => (
                <button 
                    key={chat.id}
                    onClick={() => selectChat(chat.id)}
                >
                    {chat.title}
                </button>
            ))}

            {selectedChat && (
                <div>
                    <h2>{selectedChat.title}</h2>

                    {selectedChat.messages.map((message) => (
                        <div key={message.id}>
                            <strong>{message.role}</strong>
                            <p>{message.content}</p>
                        </div>
                    ))}

                    {isLoading && (
                        <p>Assistant is thinking...</p>
                    )}

                    <form onSubmit={sendMessage}>
                        <input
                            type="text"
                            value={messageInput}
                            onChange={(event) => setMessageInput(event.target.value)}
                            placeholder="Ask me about health and fitness..."
                            disabled={isLoading}
                        />

                        <button type="submit">
                            Send
                        </button>
                    </form>
                </div>
            )}
        </div>
    )
}

export default Chat