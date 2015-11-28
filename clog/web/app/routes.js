import page from 'page';
import * as views from './views';

page('/', views.index);
page('/log/:id', views.log);
