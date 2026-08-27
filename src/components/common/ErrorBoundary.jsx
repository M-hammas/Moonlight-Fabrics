import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("Sidra Fabrics application error:", error, info);
  }

  handleReload = () => window.location.reload();

  render() {
    if (!this.state.hasError) return this.props.children;

    const message = this.state.error?.message || "An unexpected application error occurred.";

    return (
      <main
        style={{
          minHeight: "100vh",
          display: "grid",
          placeItems: "center",
          padding: "32px",
          background: "#f6f6f4",
          color: "#111",
          fontFamily: "Arial, Helvetica, sans-serif",
        }}
      >
        <section
          style={{
            width: "min(680px, 100%)",
            background: "#fff",
            border: "1px solid #ddd",
            padding: "36px",
            boxShadow: "0 16px 50px rgba(0,0,0,.08)",
          }}
        >
          <p style={{ margin: 0, fontSize: 11, letterSpacing: ".18em", fontWeight: 700, color: "#777" }}>
            SIDRA FABRICS / APPLICATION ERROR
          </p>
          <h1 style={{ fontSize: "clamp(34px, 7vw, 64px)", lineHeight: 0.98, letterSpacing: "-.05em", margin: "18px 0" }}>
            The page hit an unexpected error.
          </h1>
          <p style={{ color: "#666", lineHeight: 1.7 }}>
            The development server is running, but a frontend component failed during rendering.
            The error is shown below instead of leaving you with a blank white screen.
          </p>
          <pre style={{ overflow: "auto", padding: 16, background: "#f5f5f5", border: "1px solid #e5e5e5", whiteSpace: "pre-wrap" }}>
            {message}
          </pre>
          <button
            type="button"
            onClick={this.handleReload}
            style={{ marginTop: 14, background: "#111", color: "#fff", border: 0, padding: "13px 18px", cursor: "pointer" }}
          >
            Reload application
          </button>
        </section>
      </main>
    );
  }
}
