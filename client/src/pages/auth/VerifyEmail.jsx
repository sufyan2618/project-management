import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const VerifyEmail = () => {
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resendLoading, setResendLoading] = useState(false);
  const [resendMessage, setResendMessage] = useState('');
  const [cooldown, setCooldown] = useState(0);
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email;

  useEffect(() => {
    if (!email) {
      navigate('/register');
    }
  }, [email, navigate]);

  useEffect(() => {
    if (cooldown > 0) {
      const timer = setTimeout(() => setCooldown(cooldown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [cooldown]);

  const handleVerify = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/verify-otp',
        null,
        {
          params: { email, otp }
        }
      );

      if (response.data.success) {
        navigate('/login', { 
          state: { message: 'Email verified successfully! Please login.' } 
        });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Verification failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setResendMessage('');
    setError('');
    setResendLoading(true);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/resend-otp',
        null,
        {
          params: { email }
        }
      );

      if (response.data.success) {
        setResendMessage('OTP sent successfully! Please check your email.');
        setCooldown(60);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to resend OTP';
      
      // Check if it's a rate limit error
      if (err.response?.status === 429) {
        setError(errorMsg);
        // Extract wait time from error message if present
        const match = errorMsg.match(/(\d+) seconds/);
        if (match) {
          setCooldown(parseInt(match[1]));
        }
      } else {
        setError(errorMsg);
      }
    } finally {
      setResendLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Verify Your Email
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            We've sent a verification code to
            <span className="font-medium text-indigo-600"> {email}</span>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleVerify}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {resendMessage && (
            <div className="rounded-md bg-green-50 p-4">
              <p className="text-sm text-green-800">{resendMessage}</p>
            </div>
          )}

          <div>
            <label htmlFor="otp" className="block text-sm font-medium text-gray-700">
              Verification Code
            </label>
            <input
              id="otp"
              name="otp"
              type="text"
              required
              maxLength="6"
              className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Enter 6-digit code"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading || otp.length !== 6}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Verifying...
                </span>
              ) : (
                'Verify Email'
              )}
            </button>
          </div>

          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={handleResendOTP}
              disabled={resendLoading || cooldown > 0}
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500 disabled:text-gray-400 disabled:cursor-not-allowed"
            >
              {resendLoading ? (
                'Sending...'
              ) : cooldown > 0 ? (
                `Resend OTP (${cooldown}s)`
              ) : (
                'Resend OTP'
              )}
            </button>

            <button
              type="button"
              onClick={() => navigate('/login')}
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              Back to Login
            </button>
          </div>
        </form>

        <div className="mt-4 text-center text-xs text-gray-500">
          <p>Didn't receive the code? Check your spam folder.</p>
          <p className="mt-1">The code expires in 5 minutes.</p>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmail;
