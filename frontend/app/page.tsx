'use client';

import React, { useState } from 'react';
import { CopilotTextarea } from '@copilotkit/react-textarea';
import { Send, Utensils, MapPin } from 'lucide-react';

export default function RestaurantFinder() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState('San Francisco');

  const handleSubmit = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, location }),
      });

      const data = await res.json();

      if (data.generateCopilotResponse?.messages?.length > 0) {
        const assistantMessage = {
          role: 'assistant',
          content: data.generateCopilotResponse.messages[0].content,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `Error: ${error.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc', padding: '20px' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1
            style={{
              fontSize: '2.5rem',
              fontWeight: 'bold',
              color: '#1f2937',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
            }}
          >
            <Utensils size={40} color="#3b82f6" />
            Restaurant Finder
          </h1>
          <p style={{ color: '#6b7280', fontSize: '1.1rem' }}>
            AI-powered restaurant discovery with CrewAI + CopilotKit
          </p>
        </div>

        {/* Location Selector */}
        <div
          style={{
            background: 'white',
            padding: '20px',
            borderRadius: '12px',
            marginBottom: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <MapPin size={20} color="#3b82f6" />
            <label style={{ fontWeight: '600', color: '#374151' }}>
              Location:
            </label>
            <select
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                border: '1px solid #d1d5db',
                fontSize: '14px',
              }}
            >
              <option>San Francisco</option>
              <option>New York City</option>
              <option>Los Angeles</option>
              <option>Chicago</option>
              <option>Miami</option>
            </select>
          </div>
        </div>

        {/* Chat Area */}
        <div
          style={{
            background: 'white',
            borderRadius: '12px',
            padding: '20px',
            minHeight: '400px',
            marginBottom: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          {messages.length === 0 ? (
            <div
              style={{
                textAlign: 'center',
                color: '#6b7280',
                paddingTop: '100px',
              }}
            >
              <Utensils
                size={48}
                color="#d1d5db"
                style={{ marginBottom: '16px' }}
              />
              <p>Ask me to find restaurants in {location}!</p>
              <p style={{ fontSize: '14px', marginTop: '8px' }}>
                Try: "Find me the best Italian restaurants" or "I want sushi
                places"
              </p>
            </div>
          ) : (
            <div>
              {messages.map((msg, index) => (
                <div
                  key={index}
                  style={{
                    marginBottom: '16px',
                    display: 'flex',
                    justifyContent:
                      msg.role === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <div
                    style={{
                      maxWidth: '80%',
                      padding: '12px 16px',
                      borderRadius: '12px',
                      background: msg.role === 'user' ? '#3b82f6' : '#f3f4f6',
                      color: msg.role === 'user' ? 'white' : '#1f2937',
                    }}
                  >
                    <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div style={{ textAlign: 'center', color: '#6b7280' }}>
                  <div>🤖 AI agents are finding restaurants...</div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div
          style={{
            background: 'white',
            borderRadius: '12px',
            padding: '16px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            display: 'flex',
            gap: '12px',
          }}
        >
          <CopilotTextarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Find restaurants in ${location}...`}
            style={{
              flex: 1,
              padding: '12px',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              outline: 'none',
              resize: 'none',
            }}
            rows={2}
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !input.trim()}
            style={{
              padding: '12px 20px',
              background: loading || !input.trim() ? '#d1d5db' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <Send size={16} />
            {loading ? 'Finding...' : 'Find'}
          </button>
        </div>

        <div
          style={{
            textAlign: 'center',
            marginTop: '20px',
            fontSize: '12px',
            color: '#9ca3af',
          }}
        >
          Powered by CrewAI + CopilotKit • Code reviewed by CodeRabbit
        </div>
      </div>
    </div>
  );
}
