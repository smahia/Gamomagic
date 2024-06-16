import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { Game } from './service-output';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private ENDPOINT = environment.backendUrl;

  baseUrl = this.ENDPOINT; // Remember to change to localhost in local development
  headers = new HttpHeaders({
    'Access-Control-Allow-Origin': '*'
  });
  options = {
    mode: 'no-cors',
    headers: this.headers
  };

  getGames(http: HttpClient): Observable<Game[]> {
    return http.get<Game[]>(this.baseUrl + '/getGames', this.options).pipe(
      catchError(error => {
        console.error('Error fetching games:', error);
        return [];
      })
    );
  }

  getRegions(http: HttpClient): Observable<Game[]> {
    return http.get<Game[]>(this.baseUrl + '/getRegions', this.options).pipe(
      catchError(error => {
        console.error('Error fetching regions:', error);
        return [];
      })
    );
  }

  getPlatforms(http: HttpClient): Observable<Game[]> {
    return http.get<Game[]>(this.baseUrl + '/getPlatforms', this.options).pipe(
      catchError(error => {
        console.error('Error fetching platforms:', error);
        return [];
      })
    );
  }

  searchGame(http: HttpClient, game: Game): Observable<any>  {
    return http.post(this.baseUrl + '/search', game, this.options).pipe(
      tap(message => console.log(message)),
      catchError(_ => of(null))
    );
  }

  deleteGame(http: HttpClient, game: Game): Observable<any>  {
    return http.post(this.baseUrl + '/delete', game, this.options).pipe(
      tap(message => console.log(message)),
      catchError(_ => of(null))
    );
  }

  insertGame(http: HttpClient, game: Game): Observable<any>  {
    return http.post(this.baseUrl + '/insert', game, this.options).pipe(
      tap(message => console.log(message)),
      catchError(_ => of(null))
    );
  }

  updateGame(http: HttpClient, game: Game): Observable<any>  {
    return http.post(this.baseUrl + '/update', game, this.options).pipe(
      tap(message => console.log(message)),
      catchError(_ => of(null))
    );
  }

  // TODO: You can use this, for example, to show a game in another view!
  // async getGameById(id: number): Promise<ServiceOutput | undefined> {
  //   const data = await fetch(`${this.url}/${id}`);
  //   return await data.json() ?? {};
  // }
}
