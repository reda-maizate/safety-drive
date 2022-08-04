import type { NextPage } from 'next';
import Head from 'next/head';
import Layout from '../components/layout/Layout';
import Register from '../components/layout/Register';

export default function register() {
    return (
      <Layout>
        <Head>
          <title>Register Page</title>
          <meta name="description" content="Safety drive register page" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Register />
      </Layout>
    )
}