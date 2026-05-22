import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8001";

export default function Dashboard() {

    const [data, setData] = useState(null);

    useEffect(() => {
        fetchAnalytics();
    }, []);

    const fetchAnalytics = async () => {
        try {
            const res = await axios.get(`${API}/analytics/summary`);
            setData(res.data);
        } catch (err) {
            console.log(err);
        }
    };

    if (!data) {
        return (
            <div style={{ color: "white", padding: "40px" }}>
                Loading dashboard...
            </div>
        );
    }

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#020617",
                color: "white",
                padding: "30px",
            }}
        >
            <h1 style={{ marginBottom: "30px" }}>
                Ollive Observability Dashboard
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(4, 1fr)",
                    gap: "20px",
                    marginBottom: "40px",
                }}
            >
                <Card
                    title="Total Requests"
                    value={data.total_requests}
                />

                <Card
                    title="Success Requests"
                    value={data.success_requests}
                />

                <Card
                    title="Failed Requests"
                    value={data.failed_requests}
                />

                <Card
                    title="Avg Latency"
                    value={`${Number(data.avg_latency).toFixed(2)}s`}
                />
            </div>

            <div
                style={{
                    background: "#0f172a",
                    padding: "20px",
                    borderRadius: "16px",
                }}
            >
                <h2 style={{ marginBottom: "20px" }}>
                    Recent Logs
                </h2>

                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse",
                    }}
                >
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Model</th>
                            <th>Status</th>
                            <th>Latency</th>
                            <th>Tokens</th>
                        </tr>
                    </thead>

                    <tbody>
                        {data.recent_logs.map((log) => (
                            <tr key={log.id}>
                                <td>{log.id}</td>
                                <td>{log.model}</td>
                                <td>{log.status}</td>
                                <td>
                                    {Number(log.latency).toFixed(2)}s
                                </td>
                                <td>{log.tokens}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function Card({ title, value }) {
    return (
        <div
            style={{
                background: "#0f172a",
                padding: "24px",
                borderRadius: "16px",
            }}
        >
            <div
                style={{
                    color: "#94a3b8",
                    marginBottom: "10px",
                }}
            >
                {title}
            </div>

            <div
                style={{
                    fontSize: "32px",
                    fontWeight: "bold",
                }}
            >
                {value}
            </div>
        </div>
    );
}