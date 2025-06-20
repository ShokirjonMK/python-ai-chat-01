import React from 'react';
import { GoogleLogin, googleLogout } from '@react-oauth/google';
import axios from 'axios';

function Login({ onLogin }: { onLogin: (user: any) => void }) {
  return (
    <GoogleLogin
      onSuccess={credentialResponse => {
        axios.post("http://localhost:8000/auth/google", {
          token: credentialResponse.credential
        }).then(res => {
          onLogin(res.data);
        });
      }}
      onError={() => {
        console.log('Login Failed');
      }}
    />
  );
}

export default Login;
