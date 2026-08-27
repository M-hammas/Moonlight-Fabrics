import React from 'react';export default function Toast({message,onClose}){if(!message)return null;return <div className="toast"><span>✓</span>{message}<button onClick={onClose}>×</button></div>}
