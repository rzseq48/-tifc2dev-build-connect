import { useState } from "react";

export default function TicketForm({ onCreate }) {
  const [data, setData] = useState({
    title: "",
    description: "",
    priority: "Medium",
    category: "General",
  });
  const [message, setMessage] = useState("");

  async function submit(event) {
    event.preventDefault();
    setMessage("");

    try {
      const created = await onCreate({
        ...data,
        title: data.title.trim(),
        description: data.description.trim(),
      });

      setMessage(`Created ticket ${created.id}.`);
      setData({
        title: "",
        description: "",
        priority: "Medium",
        category: "General",
      });
    } catch (error) {
      setMessage(
        error.response?.data?.error || error.message || "Create failed."
      );
    }
  }

  return (
    <form onSubmit={submit}>
      <h2>Create ticket</h2>

      <input
        placeholder="Title"
        value={data.title}
        onChange={(event) =>
          setData({ ...data, title: event.target.value })
        }
      />

      <textarea
        placeholder="Description"
        value={data.description}
        onChange={(event) =>
          setData({ ...data, description: event.target.value })
        }
      />

      <select
        value={data.priority}
        onChange={(event) =>
          setData({ ...data, priority: event.target.value })
        }
      >
        <option>Low</option>
        <option>Medium</option>
        <option>High</option>
      </select>

      <input
        placeholder="Category"
        value={data.category}
        onChange={(event) =>
          setData({ ...data, category: event.target.value })
        }
      />

      <button type="submit">Create</button>
      {message && <p>{message}</p>}
    </form>
  );
}