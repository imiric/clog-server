import 'normalizecss/normalize.css';
import './styles/base.css';
import 'skeleton-css/css/skeleton.css';
import './styles/main.css';

import $ from 'domtastic';
import page from 'page';

import './routes';


$(document).ready(() => {
  page();
});
