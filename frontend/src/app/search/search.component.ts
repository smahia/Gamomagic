import { Component, inject, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatPaginatorModule } from '@angular/material/paginator';

import { Game, GameImpl } from './service-output';
import { SearchService } from './search.service';
import { AlertComponent } from '../alert/alert.component';
import { AlertService } from '../alert/alert.service';
import { ModalComponent } from '../modal/modal.component';
import { ModalService } from '../modal/modal.service';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    AlertComponent,
    ModalComponent,
    CommonModule,
    HttpClientModule,
    FormsModule,
    MatPaginatorModule,
  ],
  templateUrl: 'search.component.html',
  styleUrls: ['search.component.css'],
})

export class SearchComponent {
  alertService: AlertService = inject(AlertService);

  modalService: ModalService = inject(ModalService);
  game_modal: Game = new GameImpl();

  searchService: SearchService = inject(SearchService);
  gameList: Game[] = [];
  filteredGameList: Game[] = [];
  regionList: Game[] = [];
  platformList: Game[] = [];

  @ViewChild('filterSearch') searchBar: ElementRef;
  @ViewChild('filterPlatform') searchPlatform: ElementRef;

  pageSize = 10;
  pageIndex = 0;
  pageSizeOptions: number[] = [10, 25, 50, 100];

  constructor(private http: HttpClient) {
    // On the first load, get all games/regions/platforms
    this.searchService.getGames(this.http).subscribe((gameList: Game[]) => {
      this.gameList = gameList;
      this.filteredGameList = gameList;
    });
    this.searchService.getRegions(this.http).subscribe((regionList: Game[]) => {
      this.regionList = regionList;
    })
    this.searchService.getPlatforms(this.http).subscribe((platformList: Game[]) => {
      this.platformList = platformList;
      const defaultPlatform = new GameImpl();
      defaultPlatform.game_platform = 'All';
      this.platformList.push(defaultPlatform);
    })
    this.searchBar = inject(ElementRef);
    this.searchPlatform = inject(ElementRef);
  }

  // For debug purposes. Local search.
  filterResults(text: string) {
    if (!text) {
      this.filteredGameList = this.gameList;
    }

    this.filteredGameList = this.gameList.filter(
      game => game?.game_name.toLowerCase().includes(text.toLowerCase())
    );
  }

  search(searchValue: string, platformValue: string) {
    let game = new GameImpl();
    game.game_name = searchValue;
    if (platformValue != 'All') {
      game.game_platform = platformValue;
    }

    this.searchService.searchGame(this.http, game).subscribe((gameList: Game[]) => {
      this.filteredGameList = gameList;
    })
  }

  reset() {
    // Clear input value of the search bar
    this.searchBar.nativeElement.value = '';
    this.searchPlatform.nativeElement.value = 'All';
    this.filteredGameList = this.gameList; // Restore the whole list of games
  }

  openModalDelete(game: Game) {
    // First fill the variables of modal
    this.game_modal.game_code = game.game_code;
    this.game_modal.game_name = game.game_name;
    this.game_modal.game_platform = game.game_platform;
    this.game_modal.game_region = game.game_region;
    this.game_modal.game_language = game.game_language;

    // Open modal
    this.modalService.open('modal-delete');
  }

  delete() {
    // Close modal window: modal-modify
    this.modalService.close();

    // Delete the game: this.game_modal is filled in the modal!
    this.searchService.deleteGame(this.http, this.game_modal).subscribe((_) => {
      this.alertService.success('Game deleted', { autoClose: true });
      this.searchService.getGames(this.http).subscribe((gameList: Game[]) => {
        this.gameList = gameList;
        this.filteredGameList = gameList;
      });
    });
  }

  openModalUpdate(game: Game) {
    // First fill the variables of modal
    this.game_modal.game_code = game.game_code;
    this.game_modal.game_name = game.game_name;
    this.game_modal.game_platform = game.game_platform;
    this.game_modal.game_region = game.game_region;
    this.game_modal.game_language = game.game_language;

    // Open modal
    this.modalService.open('modal-modify');
  }

  update() {
    // Close modal window: modal-modify
    this.modalService.close();

    // Update the new game: this.game_modal is filled in the modal!
    this.searchService.updateGame(this.http, this.game_modal).subscribe((_) => {

      if (this.game_modal.game_name == '' || this.game_modal.game_platform == '') {
        this.alertService.error('Name and platform cannot be empty', { autoClose: true });
        return;

      } else {  
      // if success...
      // show alert
      this.alertService.success('Game updated', { autoClose: true });
      // refresh list of games
      this.searchService.getGames(this.http).subscribe((gameList: Game[]) => {
        this.gameList = gameList;
        this.filteredGameList = gameList;
      });

      }
    })
  }

  openModalInsert() {
    // Clear modal variable
    this.game_modal = new GameImpl();
    this.modalService.open('modal-insert');
  }

  insert() {
    // Close modal window: modal-insert
    this.modalService.close();

    // Insert the new game: this.game_modal is filled in the modal!
    this.searchService.insertGame(this.http, this.game_modal).subscribe((_) => {

      if (this.game_modal.game_name == '' || this.game_modal.game_platform == '') {
        this.alertService.error('Name and platform cannot be empty', { autoClose: true });
        return;

      } else {
        // if success...
        // show alert
        this.alertService.success('Game inserted', { autoClose: true });
        // refresh list of games
        this.searchService.getGames(this.http).subscribe((gameList: Game[]) => {
          this.gameList = gameList;
          this.filteredGameList = gameList;
        });
      }
    })
  }

  // Sort buttons
  sortUp() {
    this.filteredGameList.sort((a, b) => a.game_name.localeCompare(b.game_name));
  }
  sortDown() {
    this.filteredGameList.sort((a, b) => b.game_name.localeCompare(a.game_name));
  }

  // Paginator
  onPageChange(event: any) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
  }
}
