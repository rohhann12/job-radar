import React, { useState, useEffect } from "react";
import axios from "axios";
import { Toaster, toast } from "react-hot-toast";

function App() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title = "Job Radar";
  }, []);

  const startJobScheduler = async () => {
    if (!email) {
      toast.error("Please enter your email.");
      return;
    }

    setLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";
      const response = await axios.post(`${backendUrl}/main`, { email });
      toast.success(response.data.message || "Scheduler started.");
    } catch (error) {
      toast.error("Failed to start scheduler.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <Toaster position="top-center" />

      <div style={styles.card}>
        <div style={styles.badge}>LIVE</div>

        <svg style={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" strokeLinecap="round" />
        </svg>

        <h1 style={styles.title}>Job Radar</h1>
        <p style={styles.subtitle}>
          Crawls Google, Microsoft, Amazon, Meta, Adobe, Atlassian &amp; more every 15 mins.
          Get emailed the moment a new fresher role posts.
        </p>

        <input
          type="email"
          placeholder="your@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && startJobScheduler()}
          style={styles.input}
        />

        <button
          onClick={startJobScheduler}
          disabled={loading}
          style={loading ? { ...styles.button, opacity: 0.5 } : styles.button}
        >
          {loading ? "Starting..." : "Start Alerts"}
        </button>

        <p style={styles.hint}>Alerts sent to your inbox. Unsubscribe anytime.</p>
      </div>

      <p style={styles.footer}>© {new Date().getFullYear()} Job Radar</p>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#000",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    padding: "2rem",
  },
  card: {
    background: "#fff",
    borderRadius: "16px",
    padding: "3rem 2.5rem",
    maxWidth: "440px",
    width: "100%",
    textAlign: "center",
    position: "relative",
  },
  badge: {
    position: "absolute",
    top: "1.25rem",
    right: "1.25rem",
    background: "#000",
    color: "#fff",
    fontSize: "0.65rem",
    fontWeight: "700",
    letterSpacing: "0.1em",
    padding: "3px 8px",
    borderRadius: "4px",
  },
  icon: {
    width: "40px",
    height: "40px",
    color: "#000",
    marginBottom: "1rem",
  },
  title: {
    fontSize: "2rem",
    fontWeight: "700",
    color: "#000",
    margin: "0 0 0.75rem",
    letterSpacing: "-0.03em",
  },
  subtitle: {
    fontSize: "0.9rem",
    color: "#666",
    lineHeight: "1.6",
    margin: "0 0 2rem",
  },
  input: {
    width: "100%",
    padding: "0.85rem 1rem",
    fontSize: "0.95rem",
    border: "1.5px solid #e0e0e0",
    borderRadius: "8px",
    outline: "none",
    boxSizing: "border-box",
    marginBottom: "0.75rem",
    color: "#000",
    background: "#fafafa",
  },
  button: {
    width: "100%",
    padding: "0.85rem",
    fontSize: "0.95rem",
    fontWeight: "600",
    background: "#000",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    letterSpacing: "0.01em",
  },
  hint: {
    marginTop: "1rem",
    fontSize: "0.78rem",
    color: "#aaa",
  },
  footer: {
    marginTop: "2rem",
    fontSize: "0.78rem",
    color: "#444",
  },
};

export default App;
