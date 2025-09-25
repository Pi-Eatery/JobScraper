import React, { useState, useEffect } from 'react';
import {
  fetchKeywords,
  addKeyword,
  deleteKeyword,
} from '../../services/keywordService';

const KeywordManager = () => {
  const [keywords, setKeywords] = useState([]);
  const [newKeyword, setNewKeyword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadKeywords();
  }, []);

  const loadKeywords = async () => {
    try {
      setLoading(true);
      const data = await fetchKeywords();
      setKeywords(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddKeyword = async (e) => {
    e.preventDefault();
    if (!newKeyword.trim()) return;

    try {
      await addKeyword(newKeyword);
      setNewKeyword('');
      loadKeywords(); // Reload keywords after adding
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteKeyword = async (keywordId) => {
    try {
      await deleteKeyword(keywordId);
      loadKeywords(); // Reload keywords after deleting
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div>Loading keywords...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div className="keyword-manager-container">
      <h2>Manage Keywords</h2>

      <form onSubmit={handleAddKeyword}>
        <input
          type="text"
          value={newKeyword}
          onChange={(e) => setNewKeyword(e.target.value)}
          placeholder="Add new keyword"
        />
        <button type="submit">Add Keyword</button>
      </form>

      {keywords.length === 0 ? (
        <p>No keywords found. Add some to start scraping!</p>
      ) : (
        <ul>
          {keywords.map((keyword) => (
            <li key={keyword.id}>
              {keyword.term}
              <button onClick={() => handleDeleteKeyword(keyword.id)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default KeywordManager;
