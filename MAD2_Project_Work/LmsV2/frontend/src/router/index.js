import { createRouter, createWebHistory } from 'vue-router';

import LoginForm from '@/components/LoginForm.vue';
import DashboardPage from '@/components/DashboardPage.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import SuccessPage from '@/components/SuccessPage.vue'
import BookDetails from '@/components/BookDetails.vue'
import AdminHome from '@/components/AdminHome.vue'
import UpdateDetails from '@/components/UpdateDetails.vue'
import UpdateBook from '@/components/UpdateBook.vue';
import DeleteAccount from '@/components/DeleteAccount.vue'
import AlreadyExist from '@/components/AlreadyExist.vue'
import DeleteBook from '@/components/DeleteBook.vue'
import StudentDetails from '@/components/StudentDetails.vue';
import ShowBook from '@/components/ShowBook.vue';
import PendingReturns from '@/components/PendingReturns.vue';
import BackPack from '@/components/BackPack.vue';
import GotoLibrary from '@/components/GotoLibrary.vue'
import StatisticsHome from '@/components/StatisticsHome.vue';
import TransActions from '@/components/TransActions.vue';
import BookWise from '@/components/BookWise.vue';
import StatisticsSect from '@/components/StatisticsSect.vue';
import SectionsOptions from '@/components/SectionsOptions.vue';
import NotFound from '@/components/NotFound.vue';


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    {
      name: "LoginForm",
      component: LoginForm,
      path: "/",
    },
    {
      name: "DashboardPage",
      component: DashboardPage,
      path: "/dashboard"
    },
    {
      name: "RegisterForm",
      component: RegisterForm,
      path: "/registerForm"
    },
    {
      name: "SuccessPage",
      component: SuccessPage,
      path: "/successPage/:succ_id",
    },
    {
      name: "BookDetails",
      component: BookDetails,
      path: "/book_details/:book_id"
    },
    {
      name: "AdminHome",
      component: AdminHome,
      path: "/admin_home"
    },
    {
      name: "GotoLibrary",
      component: GotoLibrary,
      path: "/GotoLibrary"
    },
    {
      name: "SectionsOptions",
      component: SectionsOptions,
      path: "/SectionsOptions"
    },
    {
      name: "UpdateDetails",
      component: UpdateDetails,
      path: "/UpdateDetails/:role/:email",
    },
    {
      name: "DeleteAccount",
      component: DeleteAccount,
      path: "/DeleteAccount/:role/:email",
    },
    {
      name: "AlreadyExist",
      component: AlreadyExist,
      path: "/AlreadyExist/:book_id",
    },
    {
      name: "UpdateBook",
      component: UpdateBook,
      path: "/UpdateBook/:book_id",
    },
    {
      name: "DeleteBook",
      component: DeleteBook,
      path: "/DeleteBook/:book_id",
    },
    {
      name: 'StudentDetails',
      component: StudentDetails,
      path: "/StudentDetails/:email",
    },
    {
      name: 'ShowBook',
      component: ShowBook,
      path: "/ShowBook/:book_id",
    },
    {
      name: 'PendingReturns',
      component: PendingReturns,
      path: "/PendingReturns",
    },
    {
      name: 'BackPack',
      component: BackPack,
      path: "/BackPack",
    },
    {
      name: 'StatisticsHome',
      component: StatisticsHome,
      path: "/StatisticsHome",
    },
    {
      name: 'BookWise',
      component: BookWise,
      path: "/BookWise",
    },
    {
      name: 'StatisticsSect',
      component: StatisticsSect,
      path: "/StatisticsSect",
    },
    {
      name: 'TransActions',
      component: TransActions,
      path: "/TransActions",
    },
    {
      path: '/:pathMatch(.*)*',  // Catch-all route for undefined paths
      name: 'NotFound',
      component: NotFound,
    },
  ]

});

export default router;