import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Job Application Tracker heading', () => {
  render(<App />);
  const headingElement = screen.getByLabelText(/Job Application Tracker Heading/i);
  expect(headingElement).toBeInTheDocument();
});
