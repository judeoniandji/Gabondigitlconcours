import { render, screen } from '@testing-library/react';
jest.mock('./services/api', () => ({
  __esModule: true,
  default: {
    interceptors: { request: { use: () => {} } },
    post: () => Promise.resolve({ data: {} }),
    get: () => Promise.resolve({ data: [] }),
  },
}));
import App from './App';

test('affiche la page de connexion', () => {
  render(<App />);
  const heading = screen.getByText(/Connexion/i);
  expect(heading).toBeInTheDocument();
});
