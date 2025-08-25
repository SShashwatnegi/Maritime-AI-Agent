import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with detailed config
const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      headers: config.headers,
      data: config.data
    });
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', {
      status: response.status,
      data: response.data,
      url: response.config.url
    });
    return response;
  },
  (error) => {
    console.error('❌ API Error:', {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      data: error.response?.data,
      config: error.config
    });
    
    // Provide more specific error messages
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      throw new Error('Cannot connect to API server. Make sure your backend is running on http://localhost:8000');
    }
    
    return Promise.reject(error);
  }
);

// Test function to check API connectivity
const testConnection = async () => {
  try {
    console.log('🔍 Testing API connection to:', API_BASE);
    const response = await fetch(`${API_BASE.replace('/api', '')}/health`, {
      method: 'GET',
      mode: 'cors',
    });
    console.log('🏥 Health check response:', response.status);
    return response.ok;
  } catch (error) {
    console.error('🚨 Connection test failed:', error);
    return false;
  }
};

export const maritimeAPI = {
  // Test connection
  testConnection,

  // Agentic AI endpoints
  agentQuery: async (query, file = null, context = null) => {
    console.log('🤖 Agent Query Request:', { query, hasFile: !!file, context });
    
    const formData = new FormData();
    formData.append('query', query);
    if (file) {
      formData.append('file', file);
      console.log('📁 File attached:', file.name, file.size);
    }
    if (context) formData.append('context', JSON.stringify(context));

    try {
      const response = await api.post('/agent/query', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          // Remove any existing Content-Type to let browser set it with boundary
        },
        timeout: 60000 // Increase timeout for agent queries
      });
      return response.data;
    } catch (error) {
      console.error('🚨 Agent Query Error:', error);
      throw error;
    }
  },

  getAgentStatus: async () => {
    try {
      const response = await api.get('/agent/status');
      return response.data;
    } catch (error) {
      console.error('🚨 Agent Status Error:', error);
      throw error;
    }
  },

  getAgentExamples: async () => {
    try {
      const response = await api.get('/agent/examples');
      return response.data;
    } catch (error) {
      console.error('🚨 Agent Examples Error:', error);
      throw error;
    }
  },

  getAgentMemory: async () => {
    try {
      const response = await api.get('/agent/memory');
      return response.data;
    } catch (error) {
      console.error('🚨 Agent Memory Error:', error);
      throw error;
    }
  },

  clearAgentMemory: async () => {
    try {
      const response = await api.post('/agent/memory/clear');
      return response.data;
    } catch (error) {
      console.error('🚨 Clear Memory Error:', error);
      throw error;
    }
  },

  getAvailableTools: async () => {
    try {
      const response = await api.get('/agent/tools');
      return response.data;
    } catch (error) {
      console.error('🚨 Available Tools Error:', error);
      throw error;
    }
  },

  getComparison: async () => {
    try {
      const response = await api.get('/agent/comparison');
      return response.data;
    } catch (error) {
      console.error('🚨 Comparison Error:', error);
      throw error;
    }
  },

  // Direct tool endpoints
  askDirect: async (query) => {
    try {
      console.log('🧠 Direct AI Query:', query);
      const response = await api.post('/ask', { query });
      return response.data;
    } catch (error) {
      console.error('🚨 Direct AI Error:', error);
      throw error;
    }
  },

  summarizeDocument: async (file) => {
    try {
      console.log('📄 Document Summary Request:', file.name);
      const formData = new FormData();
      formData.append('file', file);
      const response = await api.post('/documents/summarize', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('🚨 Document Summary Error:', error);
      throw error;
    }
  },

  getWeather: async (lat, lon) => {
    try {
      console.log('🌤️ Weather Request:', { lat, lon });
      const response = await api.get(`/weather/${lat}/${lon}`);
      return response.data;
    } catch (error) {
      console.error('🚨 Weather Error:', error);
      throw error;
    }
  },

  // Health check
  ping: async () => {
    try {
      console.log('🏓 Ping Request');
      const response = await api.get('/ping');
      return response.data;
    } catch (error) {
      console.error('🚨 Ping Error:', error);
      throw error;
    }
  }
};

export default maritimeAPI;